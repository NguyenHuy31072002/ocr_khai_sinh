
from ultralytics import YOLO
from app.vietocr.vietocr.tool.predictor import Predictor
from app.vietocr.vietocr.tool.config import Cfg
import cv2
from typing import Dict, List, Optional, Set, Tuple
import torch
from PIL import Image
import numpy as np
import logging
from pathlib import Path
from functools import lru_cache
import re

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class OCRExtractor:
    """OCR Extractor for Vietnamese Birth Certificate with optimizations"""
    
    # Constants
    DEFAULT_PADDING = 2
    MIN_CONFIDENCE_THRESHOLD = 0.3
    
    def __init__(
        self, 
        yolo_model_path: str = "/home/admin1/Code/ocr_khai_sinh/app/model_yolov11/best.pt",
        # yolo_model_path: str = "/workspace/app/model_yolov11/best.pt",
        extract_fields: Optional[Set[str]] = None,
        class_mapping: Optional[Dict[int, str]] = None,
        batch_size: int = 1,
        use_half_precision: bool = False
    ):
        """
        Initialize YOLO model and VietOCR
        
        Args:
            yolo_model_path: Path to trained YOLO model
            extract_fields: Set of fields to extract. If None, extract all
            class_mapping: Custom class mapping (optional)
            batch_size: Batch size for processing multiple images
            use_half_precision: Use FP16 for faster inference (GPU only)
        """
        self._validate_model_path(yolo_model_path)
        
        # Device setup
        self.device = 'cuda' if torch.cuda.is_available() else 'cpu'
        logger.info(f"Using device: {self.device}")
        
        # Load YOLO model with error handling
        try:
            self.yolo_model = YOLO(yolo_model_path)
            if use_half_precision and self.device == 'cuda':
                self.yolo_model.model.half()
                logger.info("Using FP16 precision")
        except Exception as e:
            logger.error(f"Failed to load YOLO model: {e}")
            raise
        
        # Configure VietOCR
        self.ocr_predictor = self._initialize_ocr()
        
        # Class mapping
        self.class_mapping = class_mapping or {
            0: 'k_name',      
            1: 'Họ và tên',      
            2: 'k_m_name',            
            3: 'Họ và tên Mẹ',         
            4: 'k_c_name',    
            5: 'Họ và tên Cha',       
            6: 'object',      
        }
        
        self.extract_fields = extract_fields
        self.batch_size = batch_size
        
    def _validate_model_path(self, path: str) -> None:
        """Validate model file exists"""
        if not Path(path).exists():
            raise FileNotFoundError(f"Model not found: {path}")
    
    def _initialize_ocr(self) -> Predictor:
        """Initialize VietOCR with error handling"""
        try:
            config = Cfg.load_config_from_name('vgg_transformer')
            config['cnn']['pretrained'] = False
            config['device'] = self.device
            config['predictor']['beamsearch'] = False
            return Predictor(config)
        except Exception as e:
            logger.error(f"Failed to initialize OCR: {e}")
            raise
    
    def preprocess_image(self, image: Image.Image) -> np.ndarray:
        """
        Preprocess image with validation
        
        Args:
            image: PIL Image
            
        Returns:
            Numpy array in RGB format
        """
        if image is None:
            raise ValueError("Image cannot be None")
        
        # Convert to RGB if needed
        if image.mode != 'RGB':
            image = image.convert('RGB')
        
        return np.array(image)
    
    def detect_fields(
        self, 
        image: np.ndarray,
        conf_threshold: float = MIN_CONFIDENCE_THRESHOLD
    ) -> List[Dict]:
        """
        Detect fields on birth certificate with confidence filtering
        
        Args:
            image: Input image array
            conf_threshold: Minimum confidence threshold
            
        Returns:
            List of detected boxes with labels
        """
        try:
            results = self.yolo_model.predict(
                image, 
                verbose=False,
                conf=conf_threshold
            )
            
            detections = []
            for result in results:
                boxes = result.boxes
                if boxes is None:
                    continue
                    
                for box in boxes:
                    x1, y1, x2, y2 = box.xyxy[0].cpu().numpy()
                    conf = float(box.conf[0])
                    cls = int(box.cls[0])
                    
                    # Validate bbox
                    if self._is_valid_bbox([x1, y1, x2, y2]):
                        detections.append({
                            'bbox': [int(x1), int(y1), int(x2), int(y2)],
                            'confidence': conf,
                            'class_id': cls,
                            'field_name': self.class_mapping.get(cls, f'unknown_{cls}')
                        })
            
            return detections
            
        except Exception as e:
            logger.error(f"Detection failed: {e}")
            return []
    
    def _is_valid_bbox(self, bbox: List[float]) -> bool:
        """Validate bounding box coordinates"""
        x1, y1, x2, y2 = bbox
        return x2 > x1 and y2 > y1 and all(coord >= 0 for coord in bbox)
    
    def crop_and_ocr(
        self, 
        image: np.ndarray, 
        bbox: List[int],
        padding: int = DEFAULT_PADDING
    ) -> str:
        """
        Crop region and perform OCR with error handling
        
        Args:
            image: Original image
            bbox: [x1, y1, x2, y2]
            padding: Padding around bbox
            
        Returns:
            Extracted text
        """
        try:
            x1, y1, x2, y2 = bbox
            h, w = image.shape[:2]
            
            # Apply padding with boundary checks
            x1 = max(0, x1 - padding)
            y1 = max(0, y1 - padding)
            x2 = min(w, x2 + padding)
            y2 = min(h, y2 + padding)
            
            # Crop image
            cropped = image[y1:y2, x1:x2]
            
            # Validate crop
            if cropped.size == 0:
                logger.warning(f"Empty crop for bbox: {bbox}")
                return ""
            
            # Convert to PIL Image (avoid unnecessary conversion if possible)
            if not isinstance(cropped, Image.Image):
                cropped_pil = Image.fromarray(cropped)
            else:
                cropped_pil = cropped
            
            # Perform OCR
            text = self.ocr_predictor.predict(cropped_pil)
            return text.strip()
            
        except Exception as e:
            logger.error(f"OCR failed for bbox {bbox}: {e}")
            return ""
    
    @staticmethod
    @lru_cache(maxsize=128)
    def _normalize_name(name: str) -> str:
        """Cached name normalization"""
        # Remove extra whitespace
        name = ' '.join(name.split())
        # Uppercase
        name = name.upper()
        # Remove unwanted characters
        name = re.sub(r'[_-]', ' ', name)
        name = re.sub(r'\s+', ' ', name)
        return name.strip()
    
    def post_process_text(self, field_name: str, text: str) -> str:
        """
        Post-process text based on field type
        
        Args:
            field_name: Name of the field
            text: Raw OCR text
            
        Returns:
            Processed text
        """
        if not text:
            return ""
        
        text = text.strip()
        
        # Process names
        if field_name in ['Họ và tên', 'Họ và tên Mẹ', 'Họ và tên Cha']:
            return self._normalize_name(text)
        
        # Process labels
        elif field_name in ['k_name', 'k_m_name', 'k_c_name']:
            return ' '.join(text.split())
        
        # Process object field
        elif field_name == 'object':
            text_lower = text.lower()
            if 'khai sinh' in text_lower or 'giấy khai sinh' in text_lower:
                return 'Giấy khai sinh'
            return text
        
        # Process dates
        elif any(kw in field_name.lower() for kw in ['ngày', 'date']):
            # Normalize date format
            text = re.sub(r'\s+', '', text)
            text = re.sub(r'[-]', '/', text)
            return text
        
        return text
    
    def _should_swap_parent_fields(self, extracted_info: Dict) -> bool:
        """
        Determine if parent fields should be swapped based on k_c_name
        
        Improved logic: Check both word count AND semantic meaning
        """
        if 'k_c_name' not in extracted_info:
            return False
        
        k_c_name_text = extracted_info['k_c_name']['value'].lower()
        
        # Check if k_c_name contains "mẹ" or "mother" keywords
        mother_keywords = ['mẹ', 'me', 'mother', 'má']
        has_mother_keyword = any(kw in k_c_name_text for kw in mother_keywords)
        
        # Original logic: check word count
        word_count = len(k_c_name_text.split())
        
        return word_count == 4 or has_mother_keyword
    
    def swap_parent_fields(self, extracted_info: Dict) -> Dict:
        """
        Swap father and mother fields if needed
        
        Args:
            extracted_info: Extracted information dictionary
            
        Returns:
            Updated dictionary with swapped fields if necessary
        """
        if not self._should_swap_parent_fields(extracted_info):
            return extracted_info
        
        mother_key = 'Họ và tên Mẹ'
        father_key = 'Họ và tên Cha'
        
        if mother_key in extracted_info and father_key in extracted_info:
            # Swap all attributes
            extracted_info[mother_key], extracted_info[father_key] = \
                extracted_info[father_key], extracted_info[mother_key]
            
            logger.info("Swapped parent fields based on k_c_name")
        
        return extracted_info
    
    def extract_info(
        self, 
        image: Image.Image,
        return_visualization: bool = False
    ) -> Dict:
        """
        Extract complete information from birth certificate
        
        Args:
            image: Input PIL Image
            return_visualization: If True, return annotated image
            
        Returns:
            Dictionary of extracted information
        """
        try:
            # Preprocess
            img_array = self.preprocess_image(image)
            
            # Detect fields
            detections = self.detect_fields(img_array)
            
            if not detections:
                logger.warning("No fields detected")
                return {}
            
            # Sort by confidence (descending)
            detections.sort(key=lambda x: x['confidence'], reverse=True)
            
            # Extract text from each field
            extracted_info = {}
            seen_fields = set()
            
            for detection in detections:
                field_name = detection['field_name']
                
                # Filter by extract_fields if specified
                if self.extract_fields and field_name not in self.extract_fields:
                    continue
                
                # Skip duplicate fields (keep highest confidence)
                if field_name in seen_fields:
                    continue
                
                seen_fields.add(field_name)
                bbox = detection['bbox']
                
                # Perform OCR
                text = self.crop_and_ocr(img_array, bbox)
                
                # Post-process
                text = self.post_process_text(field_name, text)
                
                if text:  # Only save non-empty results
                    extracted_info[field_name] = {
                        'value': text,
                        'confidence': detection['confidence'],
                        'bbox': bbox
                    }
            
            # Swap parent fields if needed
            extracted_info = self.swap_parent_fields(extracted_info)
            
            logger.info(f"Extracted {len(extracted_info)} fields")
            return extracted_info
            
        except Exception as e:
            logger.error(f"Extraction failed: {e}")
            return {}
    
    def batch_extract(self, images: List[Image.Image]) -> List[Dict]:
        """
        Extract information from multiple images
        
        Args:
            images: List of PIL Images
            
        Returns:
            List of extraction results
        """
        results = []
        for img in images:
            result = self.extract_info(img)
            results.append(result)
        return results
    
    def __del__(self):
        """Cleanup resources"""
        if hasattr(self, 'yolo_model'):
            del self.yolo_model
        if hasattr(self, 'ocr_predictor'):
            del self.ocr_predictor
        
        # Clear CUDA cache if available
        if torch.cuda.is_available():
            torch.cuda.empty_cache()






