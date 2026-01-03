# OCR Khai Sinh - Birth Certificate OCR System

Hệ thống OCR tự động nhận dạng và trích xuất thông tin từ giấy khai sinh sử dụng YOLO và VietOCR.

[![Python](https://img.shields.io/badge/Python-3.10-blue.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.104.1-green.svg)](https://fastapi.tiangolo.com/)
[![Docker](https://img.shields.io/badge/Docker-Ready-blue.svg)](https://www.docker.com/)

---

## 📋 Mục lục

- [Tính năng](#-tính-năng)
- [Kiến trúc hệ thống](#-kiến-trúc-hệ-thống)
- [Yêu cầu hệ thống](#-yêu-cầu-hệ-thống)
- [Cài đặt](#-cài-đặt)
  - [Cách 1: Chạy với Docker (Khuyến nghị)](#cách-1-chạy-với-docker-khuyến-nghị)
  - [Cách 2: Chạy thường (Local)](#cách-2-chạy-thường-local)
- [Sử dụng](#-sử-dụng)
- [API Endpoints](#-api-endpoints)
- [Cấu trúc dự án](#-cấu-trúc-dự-án)
- [CI/CD](#-cicd)
- [Troubleshooting](#-troubleshooting)

---

## 🚀 Tính năng

- ✅ **Nhận dạng tự động** các trường thông tin trên giấy khai sinh
- ✅ **OCR tiếng Việt** với độ chính xác cao sử dụng VietOCR
- ✅ **Object Detection** với YOLO v11 để định vị các trường
- ✅ **RESTful API** với FastAPI
- ✅ **Docker support** với GPU acceleration
- ✅ **CI/CD** với Jenkins pipeline
- ✅ **Auto-scaling** ready

### Các trường được trích xuất:

- Họ và tên
- Họ và tên Cha
- Họ và tên Mẹ
- Ngày sinh
- Nơi sinh
- Và các trường khác...

---

## 🏗️ Kiến trúc hệ thống

```
┌─────────────────┐
│   Client/User   │
└────────┬────────┘
         │ HTTP Request
         ▼
┌─────────────────┐
│   FastAPI App   │
│   (Port 8000)   │
└────────┬────────┘
         │
    ┌────┴────┐
    │         │
    ▼         ▼
┌────────┐ ┌──────────┐
│  YOLO  │ │ VietOCR  │
│ Model  │ │  Model   │
└────────┘ └──────────┘
```

**Tech Stack:**
- **Backend**: FastAPI
- **OCR Engine**: VietOCR (Transformer-based)
- **Object Detection**: YOLOv11
- **Deep Learning**: PyTorch
- **Containerization**: Docker + Docker Compose
- **CI/CD**: Jenkins

---

## 💻 Yêu cầu hệ thống

### Tối thiểu:
- **OS**: Ubuntu 20.04+ / macOS / Windows 10+
- **RAM**: 8GB
- **Storage**: 10GB free space
- **Python**: 3.10
- **Docker**: 20.10+ (nếu chạy với Docker)

### Khuyến nghị:
- **RAM**: 16GB+
- **GPU**: NVIDIA GPU với CUDA support (cho inference nhanh hơn)
- **CUDA**: 11.8+
- **cuDNN**: 8.0+

---

## 📦 Cài đặt

### Cách 1: Chạy với Docker (Khuyến nghị)

Docker giúp đóng gói toàn bộ dependencies và chạy ổn định trên mọi môi trường.

#### Bước 1: Clone repository

```bash
git clone https://github.com/NguyenHuy31072002/ocr_khai_sinh.git
cd ocr_khai_sinh
```

#### Bước 2: Cấu hình environment (Optional)

```bash
cp .env.example .env
# Chỉnh sửa .env nếu cần
```

#### Bước 3: Build và chạy với Docker Compose

```bash
# Build image
docker-compose build

# Chạy container
docker-compose up -d

# Xem logs
docker-compose logs -f
```

#### Bước 4: Kiểm tra

```bash
# Check container status
docker-compose ps

# Test API
curl http://localhost:8128/docs
```

**Application sẽ chạy tại:**
- API: `http://localhost:8128`
- Swagger UI: `http://localhost:8128/docs`
- ReDoc: `http://localhost:8128/redoc`

#### Các lệnh Docker hữu ích:

```bash
# Stop containers
docker-compose down

# Restart containers
docker-compose restart

# View logs
docker-compose logs -f app

# Rebuild image
docker-compose build --no-cache

# Remove everything
docker-compose down -v
```

---

### Cách 2: Chạy thường (Local)

Chạy trực tiếp trên máy local mà không dùng Docker.

#### Bước 1: Clone repository

```bash
git clone https://github.com/NguyenHuy31072002/ocr_khai_sinh.git
cd ocr_khai_sinh
```

#### Bước 2: Tạo virtual environment

```bash
# Tạo virtual environment
python3.10 -m venv venv

# Activate virtual environment
# Linux/macOS:
source venv/bin/activate

# Windows:
venv\Scripts\activate
```

#### Bước 3: Cài đặt dependencies

```bash
# Upgrade pip
pip install --upgrade pip

# Cài đặt packages
pip install -r setup.txt
```

**Lưu ý:** Nếu có GPU, cài PyTorch với CUDA:
```bash
pip install torch==2.1.0 torchvision==0.16.0 --index-url https://download.pytorch.org/whl/cu118
```

#### Bước 4: Chuẩn bị model

Đảm bảo YOLO model đã có tại:
```
app/model_yolov11/best.pt
```

#### Bước 5: Chạy application

```bash
# Development mode (auto-reload)
uvicorn app.app:app --host 0.0.0.0 --port 8000 --reload

# Production mode
uvicorn app.app:app --host 0.0.0.0 --port 8000 --workers 4
```

**Application sẽ chạy tại:**
- API: `http://localhost:8000`
- Swagger UI: `http://localhost:8000/docs`

#### Bước 6: Test API

```bash
# Health check
curl http://localhost:8000/health

# Test với Python
python tests/test_api.py
```

---

## 📖 Sử dụng

### 1. Qua Swagger UI (Khuyến nghị cho testing)

1. Mở browser: `http://localhost:8128/docs` (Docker) hoặc `http://localhost:8000/docs` (Local)
2. Chọn endpoint `/extract`
3. Click **Try it out**
4. Upload ảnh giấy khai sinh
5. Click **Execute**
6. Xem kết quả JSON

### 2. Qua cURL

```bash
curl -X POST "http://localhost:8128/extract" \
  -H "accept: application/json" \
  -H "Content-Type: multipart/form-data" \
  -F "file=@/path/to/birth_certificate.jpg"
```

### 3. Qua Python

```python
import requests

url = "http://localhost:8128/extract"
files = {"file": open("birth_certificate.jpg", "rb")}

response = requests.post(url, files=files)
result = response.json()

print(result)
```

### 4. Qua Postman

1. Method: `POST`
2. URL: `http://localhost:8128/extract`
3. Body: `form-data`
4. Key: `file` (type: File)
5. Value: Chọn ảnh giấy khai sinh
6. Send

---

## 🔌 API Endpoints

### Health Check

```http
GET /health
```

**Response:**
```json
{
  "status": "ok"
}
```

### Extract Information

```http
POST /extract
```

**Request:**
- Content-Type: `multipart/form-data`
- Body: `file` (image file)

**Response:**
```json
{
  "success": true,
  "filename": "birth_cert.jpg",
  "data": {
    "Họ và tên": "NGUYỄN VĂN A",
    "Họ và tên Cha": "NGUYỄN VĂN B",
    "Họ và tên Mẹ": "TRẦN THỊ C",
    "Ngày sinh": "01/01/2020",
    "Nơi sinh": "Hà Nội"
  }
}
```

### Upload Image

```http
POST /upload
```

**Request:**
- Content-Type: `multipart/form-data`
- Body: `file` (image file)

**Response:**
- Content-Type: `image/jpeg`
- Body: Processed image

---

## 📁 Cấu trúc dự án

```
ocr_khai_sinh/
├── app/
│   ├── app.py                      # Main FastAPI application
│   ├── Ocr_extractor/
│   │   └── ocr_extractor.py       # OCR extraction logic
│   ├── routers/
│   │   └── development/
│   │       └── basic_router.py    # API routes
│   ├── core/
│   │   ├── config/
│   │   │   └── constants.py       # Configuration constants
│   │   └── middle_ware/
│   │       └── timer_middleware.py # Performance middleware
│   ├── model_yolov11/
│   │   └── best.pt                # YOLO model weights
│   └── vietocr/                   # VietOCR module
│
├── tests/
│   └── test_api.py                # API tests
│
├── scripts/
│   ├── deploy.sh                  # Deployment script
│   └── demo-pipeline.sh           # CI/CD demo script
│
├── docs/
│   └── jenkins-setup.md           # Jenkins setup guide
│
├── Dockerfile                     # Docker image definition
├── docker-compose.yml             # Docker Compose configuration
├── Jenkinsfile                    # Jenkins CI/CD pipeline
├── setup.txt                      # Python dependencies
├── .dockerignore                  # Docker ignore patterns
├── .env.example                   # Environment variables template
│
├── README.md                      # This file
├── README-CICD.md                 # CI/CD documentation
└── SETUP-JENKINS-FROM-GIT.md     # Jenkins setup from Git
```

---

## 🔄 CI/CD

Dự án đã được cấu hình Jenkins CI/CD pipeline tự động.

### Quick Start CI/CD:

```bash
# Xem hướng dẫn
cat README-CICD.md

# Setup Jenkins
./quick-setup-jenkins.sh

# Demo pipeline
./scripts/demo-pipeline.sh
```

### Pipeline Stages:

1. **Checkout** - Clone code từ Git
2. **Build** - Build Docker image
3. **Test** - Chạy automated tests
4. **Push** - Push image lên Docker registry
5. **Deploy** - Deploy lên server

**Chi tiết**: Xem [README-CICD.md](README-CICD.md)

---

## 🐛 Troubleshooting

### Application không start

**Kiểm tra:**
```bash
# Xem logs
docker-compose logs -f

# Hoặc nếu chạy local
# Check Python version
python --version  # Phải là 3.10

# Check dependencies
pip list
```

### Model không load được

**Giải pháp:**
```bash
# Kiểm tra model file tồn tại
ls -lh app/model_yolov11/best.pt

# Kiểm tra quyền
chmod 644 app/model_yolov11/best.pt
```

### Out of memory

**Giải pháp:**
- Giảm batch size
- Sử dụng GPU nếu có
- Tăng RAM cho Docker:
  ```bash
  # Docker Desktop → Settings → Resources → Memory
  ```

### Port đã được sử dụng

**Giải pháp:**
```bash
# Tìm process đang dùng port
lsof -i :8128

# Kill process
kill -9 <PID>

# Hoặc đổi port trong docker-compose.yml
ports:
  - "8129:8000"  # Đổi từ 8128 sang 8129
```

### GPU không được nhận diện

**Kiểm tra:**
```bash
# Check NVIDIA driver
nvidia-smi

# Check Docker GPU support
docker run --rm --gpus all nvidia/cuda:11.8.0-base-ubuntu22.04 nvidia-smi
```

---

## 📝 Development

### Chạy tests

```bash
# API tests
python tests/test_api.py

# Với pytest (nếu có)
pytest tests/ -v
```

### Code formatting

```bash
# Format code với black
black app/

# Lint với flake8
flake8 app/
```

### Hot reload (Development)

```bash
# Docker với hot reload
docker-compose -f docker-compose.dev.yml up

# Local với uvicorn
uvicorn app.app:app --reload
```

---

## 🤝 Contributing

1. Fork repository
2. Tạo feature branch: `git checkout -b feature/amazing-feature`
3. Commit changes: `git commit -m 'Add amazing feature'`
4. Push to branch: `git push origin feature/amazing-feature`
5. Tạo Pull Request

---

## 📄 License

This project is licensed under the MIT License.

---

## 👥 Authors

- **Nguyen Huy** - [@NguyenHuy31072002](https://github.com/NguyenHuy31072002)

---

## 🙏 Acknowledgments

- [VietOCR](https://github.com/pbcquoc/vietocr) - Vietnamese OCR toolkit
- [Ultralytics](https://github.com/ultralytics/ultralytics) - YOLO implementation
- [FastAPI](https://fastapi.tiangolo.com/) - Modern web framework

---

## 📞 Support

Nếu có vấn đề, vui lòng tạo [Issue](https://github.com/NguyenHuy31072002/ocr_khai_sinh/issues) trên GitHub.

---

**Made with ❤️ in Vietnam**
