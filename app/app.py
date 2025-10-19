from fastapi import FastAPI
from .routers.development.basic_router import basic_router

import time 
from .core.middle_ware.timer_middleware import TimerMiddleware
from app.Ocr_extractor.ocr_extractor import OCRExtractor
from app.core.config.constants import YOLO_MODEL, YOLO_LOCAL

tags_metadata = [
    {
        "name": "OCR Development",
        "description": "API OCR Development Endpoints",
    },
]

app = FastAPI(openapi_tags=tags_metadata)


app.include_router(basic_router, tags=["OCR"])

app.add_middleware(TimerMiddleware)
extractor = None
@app.on_event("startup")
async def startup_event():
    start = time.perf_counter()
    global extractor
    # Thay đổi đường dẫn này
    # extractor = OCRExtractor(yolo_model_path="/home/admin1/Code/ocr_khai_sinh/app/model_yolov11/best.pt")
    extractor = OCRExtractor(yolo_model_path=YOLO_LOCAL)
    end = time.perf_counter()
    print(f"Startup event took {end - start} seconds")