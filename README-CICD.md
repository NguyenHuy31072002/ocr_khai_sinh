# Jenkins CI/CD cho OCR Khai Sinh

Hướng dẫn nhanh để thiết lập và sử dụng Jenkins CI/CD pipeline cho dự án OCR Khai Sinh.

## 📋 Tổng quan

Pipeline tự động hóa các bước:
1. **Checkout** - Lấy code từ Git repository
2. **Build** - Build Docker image
3. **Test** - Chạy API tests
4. **Push** - Push image lên Docker registry
5. **Deploy** - Deploy lên server (chỉ với branch `main`)

## 🚀 Quick Start

### 1. Cài đặt Jenkins

```bash
# Sử dụng Docker (khuyến nghị)
docker run -d \
  --name jenkins \
  -p 8080:8080 \
  -p 50000:50000 \
  -v jenkins_home:/var/jenkins_home \
  -v /var/run/docker.sock:/var/run/docker.sock \
  jenkins/jenkins:lts
```

Truy cập: `http://localhost:8080`

### 2. Cài đặt Plugins

Vào **Manage Jenkins** → **Manage Plugins**, cài đặt:
- Docker Pipeline
- Git
- Pipeline
- SSH Agent (nếu deploy qua SSH)

### 3. Cấu hình Credentials

Vào **Manage Jenkins** → **Manage Credentials**, thêm:

| ID | Type | Mô tả |
|---|---|---|
| `docker-hub-credentials` | Username/Password | Docker Hub login |
| `docker-registry-url` | Secret text | `docker.io` |
| `deploy-host` | Secret text | IP server deploy |
| `deploy-user` | Secret text | Username server |
| `ssh-deploy-key` | SSH Key | SSH private key |

### 4. Tạo Pipeline Job

1. **New Item** → Nhập tên → Chọn **Pipeline**
2. **Pipeline** section:
   - Definition: `Pipeline script from SCM`
   - SCM: `Git`
   - Repository URL: URL của repository
   - Branch: `*/main`
   - Script Path: `Jenkinsfile`
3. **Save** và **Build Now**

## 📁 Cấu trúc Files

```
ocr-khai-sinh/
├── Jenkinsfile              # Pipeline definition
├── .dockerignore            # Files to exclude from Docker build
├── .env.example             # Environment variables template
├── docker-compose.yml       # Docker compose configuration
├── scripts/
│   └── deploy.sh           # Deployment script
├── tests/
│   └── test_api.py         # API tests
└── docs/
    └── jenkins-setup.md    # Chi tiết cài đặt Jenkins
```

## 🔧 Cấu hình

### Environment Variables

Copy `.env.example` thành `.env` và cập nhật:

```bash
cp .env.example .env
# Chỉnh sửa .env với thông tin của bạn
```

### Jenkinsfile

File `Jenkinsfile` đã được cấu hình sẵn với các stages:
- Tự động build khi có code mới
- Chạy tests trước khi deploy
- Chỉ deploy khi ở branch `main`
- Tự động cleanup Docker images

## 🧪 Testing

### Chạy tests locally

```bash
# Cài đặt dependencies
pip install requests

# Start application
docker-compose up -d

# Run tests
python tests/test_api.py
```

### Chạy deployment script

```bash
# Make script executable
chmod +x scripts/deploy.sh

# Run deployment
./scripts/deploy.sh
```

## 🔄 Workflow

### Khi push code lên repository:

1. Jenkins tự động detect thay đổi (qua webhook hoặc polling)
2. Checkout code mới nhất
3. Build Docker image với tag từ commit hash
4. Chạy automated tests
5. Nếu tests pass và branch là `main`:
   - Push image lên Docker registry
   - Deploy lên server
6. Gửi notification (nếu được cấu hình)

### Manual deployment:

```bash
# Trên server deploy
cd /opt/ocr-khai-sinh
./scripts/deploy.sh
```

## 📊 Monitoring

### Xem logs

```bash
# Jenkins logs
docker logs -f jenkins

# Application logs
docker-compose logs -f

# Specific container
docker logs -f fastapi_app_huynk
```

### Health check

```bash
# Check API
curl http://localhost:8128/docs

# Check container status
docker-compose ps
```

## 🐛 Troubleshooting

### Build fails với "Cannot connect to Docker daemon"

```bash
# Thêm Jenkins user vào docker group
sudo usermod -aG docker jenkins
sudo systemctl restart jenkins
```

### Deploy fails với SSH error

```bash
# Kiểm tra SSH connection
ssh deploy-user@deploy-host

# Thêm host vào known_hosts
ssh-keyscan -H deploy-host >> ~/.ssh/known_hosts
```

### Tests fail

```bash
# Kiểm tra application có chạy không
curl http://localhost:8000/docs

# Xem logs
docker-compose logs
```

## 📚 Tài liệu chi tiết

Xem [docs/jenkins-setup.md](docs/jenkins-setup.md) để biết:
- Hướng dẫn cài đặt chi tiết
- Cấu hình webhook
- Advanced configuration
- Troubleshooting đầy đủ

## 🔐 Security Notes

- ⚠️ Không commit file `.env` vào Git
- ⚠️ Sử dụng Jenkins credentials thay vì hardcode passwords
- ⚠️ Giới hạn access đến Jenkins server
- ⚠️ Sử dụng HTTPS cho production
- ⚠️ Thường xuyên update Jenkins và plugins

## 📞 Support

Nếu gặp vấn đề:
1. Kiểm tra [Troubleshooting section](#-troubleshooting)
2. Xem [docs/jenkins-setup.md](docs/jenkins-setup.md)
3. Kiểm tra Jenkins logs và console output
