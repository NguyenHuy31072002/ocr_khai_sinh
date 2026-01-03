# Hướng dẫn Cài đặt và Cấu hình Jenkins CI/CD

## Mục lục
1. [Cài đặt Jenkins](#1-cài-đặt-jenkins)
2. [Cài đặt Plugins](#2-cài-đặt-plugins)
3. [Cấu hình Credentials](#3-cấu-hình-credentials)
4. [Tạo Jenkins Job](#4-tạo-jenkins-job)
5. [Cấu hình Webhook](#5-cấu-hình-webhook)
6. [Troubleshooting](#6-troubleshooting)

---

## 1. Cài đặt Jenkins

### Option A: Cài đặt bằng Docker (Khuyến nghị)

```bash
# Tạo volume để lưu dữ liệu Jenkins
docker volume create jenkins_home

# Chạy Jenkins container
docker run -d \
  --name jenkins \
  -p 8080:8080 \
  -p 50000:50000 \
  -v jenkins_home:/var/jenkins_home \
  -v /var/run/docker.sock:/var/run/docker.sock \
  jenkins/jenkins:lts
```

### Option B: Cài đặt trên Ubuntu/Debian

```bash
# Thêm Jenkins repository
curl -fsSL https://pkg.jenkins.io/debian-stable/jenkins.io-2023.key | sudo tee \
  /usr/share/keyrings/jenkins-keyring.asc > /dev/null

echo deb [signed-by=/usr/share/keyrings/jenkins-keyring.asc] \
  https://pkg.jenkins.io/debian-stable binary/ | sudo tee \
  /etc/apt/sources.list.d/jenkins.list > /dev/null

# Cài đặt Jenkins
sudo apt-get update
sudo apt-get install jenkins -y

# Khởi động Jenkins
sudo systemctl start jenkins
sudo systemctl enable jenkins
```

### Truy cập Jenkins

1. Mở trình duyệt và truy cập: `http://localhost:8080`
2. Lấy initial admin password:
   ```bash
   # Nếu cài bằng Docker:
   docker exec jenkins cat /var/jenkins_home/secrets/initialAdminPassword
   
   # Nếu cài trực tiếp:
   sudo cat /var/lib/jenkins/secrets/initialAdminPassword
   ```
3. Nhập password và chọn "Install suggested plugins"
4. Tạo admin user

---

## 2. Cài đặt Plugins

Vào **Manage Jenkins** → **Manage Plugins** → **Available** và cài đặt:

### Plugins bắt buộc:
- ✅ **Docker Pipeline** - Để build và push Docker images
- ✅ **Git** - Để checkout code từ Git repository
- ✅ **Pipeline** - Để chạy Jenkinsfile
- ✅ **Credentials Binding** - Để quản lý credentials

### Plugins khuyến nghị:
- **Blue Ocean** - UI hiện đại cho Pipeline
- **GitHub Integration** - Nếu dùng GitHub
- **GitLab** - Nếu dùng GitLab
- **SSH Agent** - Để deploy qua SSH
- **Slack Notification** - Để gửi thông báo qua Slack

Sau khi cài đặt, restart Jenkins:
```bash
# Nếu dùng Docker:
docker restart jenkins

# Nếu cài trực tiếp:
sudo systemctl restart jenkins
```

---

## 3. Cấu hình Credentials

Vào **Manage Jenkins** → **Manage Credentials** → **Global** → **Add Credentials**

### 3.1. Docker Hub Credentials

- **Kind**: Username with password
- **ID**: `docker-hub-credentials`
- **Username**: Docker Hub username của bạn
- **Password**: Docker Hub password hoặc access token
- **Description**: Docker Hub Credentials

### 3.2. Docker Registry URL

- **Kind**: Secret text
- **ID**: `docker-registry-url`
- **Secret**: `docker.io` (hoặc URL registry của bạn)
- **Description**: Docker Registry URL

### 3.3. Deploy Server Credentials

#### SSH Key (Khuyến nghị)
- **Kind**: SSH Username with private key
- **ID**: `ssh-deploy-key`
- **Username**: User trên server deploy
- **Private Key**: Paste SSH private key
- **Description**: SSH Deploy Key

#### Deploy Host
- **Kind**: Secret text
- **ID**: `deploy-host`
- **Secret**: IP hoặc domain của server deploy
- **Description**: Deploy Server Host

#### Deploy User
- **Kind**: Secret text
- **ID**: `deploy-user`
- **Secret**: Username trên server deploy
- **Description**: Deploy Server User

---

## 4. Tạo Jenkins Job

### 4.1. Tạo Pipeline Job

1. Vào Jenkins dashboard → **New Item**
2. Nhập tên: `ocr-khai-sinh-pipeline`
3. Chọn **Pipeline** → **OK**

### 4.2. Cấu hình Pipeline

#### General
- ✅ Chọn **GitHub project** (nếu dùng GitHub)
- Nhập Project URL: `https://github.com/your-username/ocr-khai-sinh`

#### Build Triggers
Chọn một hoặc nhiều options:
- ✅ **GitHub hook trigger for GITScm polling** - Tự động chạy khi có push
- ✅ **Poll SCM** - Kiểm tra thay đổi định kỳ (ví dụ: `H/5 * * * *` = mỗi 5 phút)

#### Pipeline
- **Definition**: Pipeline script from SCM
- **SCM**: Git
- **Repository URL**: URL của Git repository
- **Credentials**: Thêm credentials nếu repository là private
- **Branch Specifier**: `*/main` (hoặc `*/master`)
- **Script Path**: `Jenkinsfile`

### 4.3. Lưu và Test

1. Click **Save**
2. Click **Build Now** để test pipeline
3. Xem logs tại **Console Output**

---

## 5. Cấu hình Webhook

### GitHub

1. Vào repository → **Settings** → **Webhooks** → **Add webhook**
2. **Payload URL**: `http://your-jenkins-url:8080/github-webhook/`
3. **Content type**: `application/json`
4. **Which events**: Chọn "Just the push event"
5. **Active**: ✅
6. Click **Add webhook**

### GitLab

1. Vào repository → **Settings** → **Webhooks**
2. **URL**: `http://your-jenkins-url:8080/project/ocr-khai-sinh-pipeline`
3. **Trigger**: ✅ Push events
4. **SSL verification**: Tùy chọn
5. Click **Add webhook**

---

## 6. Troubleshooting

### Lỗi: "Cannot connect to Docker daemon"

**Giải pháp**: Thêm Jenkins user vào Docker group

```bash
# Nếu cài trực tiếp:
sudo usermod -aG docker jenkins
sudo systemctl restart jenkins

# Nếu dùng Docker:
# Mount Docker socket khi chạy container (đã có trong lệnh cài đặt)
```

### Lỗi: "Permission denied" khi build Docker image

**Giải pháp**: Kiểm tra quyền Docker socket

```bash
sudo chmod 666 /var/run/docker.sock
```

### Lỗi: "Host key verification failed" khi deploy

**Giải pháp**: Thêm host vào known_hosts

```bash
# Trên Jenkins server:
ssh-keyscan -H your-deploy-server >> ~/.ssh/known_hosts
```

### Pipeline không tự động chạy khi push code

**Kiểm tra**:
1. Webhook đã được cấu hình đúng chưa?
2. Jenkins có thể truy cập được từ internet không? (nếu webhook từ GitHub/GitLab)
3. Kiểm tra **Manage Jenkins** → **System Log** để xem lỗi

**Giải pháp tạm thời**: Sử dụng Poll SCM thay vì webhook

### Build thành công nhưng deploy fail

**Kiểm tra**:
1. SSH credentials đã đúng chưa?
2. Server deploy có Docker và docker-compose chưa?
3. Port 8128 có bị block không?
4. Kiểm tra logs: `docker-compose logs -f`

---

## Các lệnh hữu ích

```bash
# Xem Jenkins logs
docker logs -f jenkins  # Nếu dùng Docker
sudo journalctl -u jenkins -f  # Nếu cài trực tiếp

# Restart Jenkins
docker restart jenkins  # Nếu dùng Docker
sudo systemctl restart jenkins  # Nếu cài trực tiếp

# Kiểm tra Jenkins status
docker ps | grep jenkins  # Nếu dùng Docker
sudo systemctl status jenkins  # Nếu cài trực tiếp

# Backup Jenkins data
docker run --rm -v jenkins_home:/data -v $(pwd):/backup ubuntu tar czf /backup/jenkins-backup.tar.gz /data
```

---

## Tài liệu tham khảo

- [Jenkins Official Documentation](https://www.jenkins.io/doc/)
- [Jenkins Pipeline Syntax](https://www.jenkins.io/doc/book/pipeline/syntax/)
- [Docker Pipeline Plugin](https://plugins.jenkins.io/docker-workflow/)
