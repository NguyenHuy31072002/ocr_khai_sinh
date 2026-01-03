from fastapi import APIRouter
from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import JSONResponse
import uvicorn
from PIL import Image
import io
import numpy as np
from app.Ocr_extractor.ocr_extractor import OCRExtractor
from fastapi import FastAPI, File, UploadFile
from fastapi.responses import StreamingResponse
from PIL import Image
import io

extractor = OCRExtractor(extract_fields={'Họ và tên Mẹ', 'k_c_name', 'k_m_name', 'Họ và tên Cha','Họ và tên'})

basic_router = APIRouter()



@basic_router.get("/health", tags=["OCR"])
async def health_check():
    return {"status": "ok"}

@basic_router.post("/extract")
async def extract_cccd_info(file: UploadFile = File(...)):
    """
    API endpoint để trích xuất thông tin từ ảnh CCCD
    """
    try:
        # Kiểm tra file type
        if not file.content_type.startswith('image/'):
            raise HTTPException(status_code=400, detail="File must be an image")
        
        # Đọc file
        contents = await file.read()
        image = Image.open(io.BytesIO(contents))
        
        # Trích xuất thông tin
        result = extractor.extract_info(image)
        
        # Format response
        response = {
            "success": True,
            "filename": file.filename,
            "data": {}
        }
        
        # Chuyển đổi format cho dễ đọc
        for field_name, info in result.items():
            response["data"][field_name] = info['value']
        
        # # Thêm metadata
        # response["metadata"] = {
        #     field_name: {
        #         "confidence": info['confidence'],
        #         "bbox": info['bbox']
        #     }
        #     for field_name, info in result.items()
        # }
        
        return JSONResponse(content=response)

    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing image: {str(e)}")

@basic_router.post("/upload")
async def upload_image(file: UploadFile = File(...)):
    # Đọc file ảnh được upload
    contents = await file.read()
    
    # Mở ảnh bằng PIL
    image = Image.open(io.BytesIO(contents))
    
    # Chuyển đổi sang RGB nếu cần (để đảm bảo format JPEG)
    if image.mode != 'RGB':
        image = image.convert('RGB')
    
    # Encode ảnh thành bytes
    img_byte_arr = io.BytesIO()
    image.save(img_byte_arr, format='JPEG')
    img_byte_arr.seek(0)
    
    # Trả về StreamingResponse
    return StreamingResponse(img_byte_arr, media_type="image/jpeg")