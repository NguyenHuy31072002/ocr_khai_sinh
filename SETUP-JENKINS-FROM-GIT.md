# 🚀 Hướng dẫn Setup Jenkins CI/CD từ Git Repository

## Tình huống: Code đã có trên Git, muốn Jenkins tự động CI/CD

### ✅ Bước 1: Cài đặt Jenkins

```bash
# Chạy Jenkins container
docker run -d \
  --name jenkins \
  -p 8080:8080 \
  -p 50000:50000 \
  -v jenkins_home:/var/jenkins_home \
  -v /var/run/docker.sock:/var/run/docker.sock \
  --user root \
  jenkins/jenkins:lts

# Đợi Jenkins khởi động (khoảng 1-2 phút)
docker logs -f jenkins
```

### ✅ Bước 2: Truy cập Jenkins

```bash
# 1. Mở browser: http://localhost:8080

# 2. Lấy password đầu tiên:
docker exec jenkins cat /var/jenkins_home/secrets/initialAdminPassword

# 3. Paste password vào browser
# 4. Chọn "Install suggested plugins"
# 5. Tạo admin user (username/password của bạn)
```

### ✅ Bước 3: Cài thêm Plugins cần thiết

1. Vào **Manage Jenkins** → **Manage Plugins**
2. Tab **Available**, tìm và cài:
   - ✅ **Docker Pipeline**
   - ✅ **Git Plugin** (thường đã có sẵn)
   - ✅ **GitHub Integration** (nếu dùng GitHub)
   - ✅ **GitLab** (nếu dùng GitLab)
3. Click **Install without restart**

### ✅ Bước 4: Cấu hình Credentials

Vào **Manage Jenkins** → **Manage Credentials** → **Global** → **Add Credentials**

#### 4.1. Git Credentials (nếu repo private)
- **Kind**: Username with password
- **ID**: `git-credentials`
- **Username**: Git username
- **Password**: Git password hoặc personal access token
- **Description**: Git Credentials

#### 4.2. Docker Hub Credentials
- **Kind**: Username with password
- **ID**: `docker-hub-credentials`
- **Username**: Docker Hub username
- **Password**: Docker Hub password
- **Description**: Docker Hub Credentials

#### 4.3. Docker Registry URL
- **Kind**: Secret text
- **ID**: `docker-registry-url`
- **Secret**: `docker.io`
- **Description**: Docker Registry URL

#### 4.4. Deploy Server (nếu có)
- **Kind**: SSH Username with private key
- **ID**: `ssh-deploy-key`
- **Username**: User trên server
- **Private Key**: Paste SSH private key
- **Description**: Deploy SSH Key

#### 4.5. Deploy Host
- **Kind**: Secret text
- **ID**: `deploy-host`
- **Secret**: IP hoặc domain server deploy
- **Description**: Deploy Host

#### 4.6. Deploy User
- **Kind**: Secret text
- **ID**: `deploy-user`
- **Secret**: Username trên server
- **Description**: Deploy User

### ✅ Bước 5: Tạo Pipeline Job

1. **Dashboard** → **New Item**
2. **Item name**: `ocr-khai-sinh-pipeline`
3. **Type**: Chọn **Pipeline**
4. Click **OK**

### ✅ Bước 6: Cấu hình Pipeline Job

#### General Section:
- ✅ **Description**: "OCR Khai Sinh CI/CD Pipeline"
- ✅ **GitHub project** (nếu dùng GitHub): Paste URL repo

#### Build Triggers:
Chọn một trong các options:

**Option A: Webhook (Tự động khi push)** - KHUYẾN NGHỊ
- ✅ **GitHub hook trigger for GITScm polling** (GitHub)
- ✅ **Build when a change is pushed to GitLab** (GitLab)

**Option B: Polling (Kiểm tra định kỳ)**
- ✅ **Poll SCM**
- Schedule: `H/5 * * * *` (check mỗi 5 phút)

**Option C: Manual**
- Không chọn gì, chỉ chạy khi click "Build Now"

#### Pipeline Section:
- **Definition**: `Pipeline script from SCM`
- **SCM**: `Git`
- **Repository URL**: `https://github.com/your-username/ocr-khai-sinh.git`
  (hoặc GitLab URL của bạn)
- **Credentials**: Chọn `git-credentials` (nếu repo private)
- **Branches to build**: `*/main` (hoặc `*/master`)
- **Script Path**: `Jenkinsfile`

### ✅ Bước 7: Cấu hình Webhook (Nếu muốn tự động)

#### Với GitHub:

1. Vào repository → **Settings** → **Webhooks** → **Add webhook**
2. **Payload URL**: `http://YOUR_JENKINS_IP:8080/github-webhook/`
   - Ví dụ: `http://192.168.1.100:8080/github-webhook/`
3. **Content type**: `application/json`
4. **Which events**: `Just the push event`
5. **Active**: ✅
6. Click **Add webhook**

#### Với GitLab:

1. Vào repository → **Settings** → **Webhooks**
2. **URL**: `http://YOUR_JENKINS_IP:8080/project/ocr-khai-sinh-pipeline`
3. **Trigger**: ✅ Push events
4. **Branch**: `main` (hoặc branch bạn muốn)
5. Click **Add webhook**

### ✅ Bước 8: Test Pipeline

1. Click **Save** trong Jenkins job config
2. Click **Build Now**
3. Xem **Console Output** để theo dõi

**Nếu thành công, bạn sẽ thấy:**
```
Stage 1: Checkout ✓
Stage 2: Build Docker Image ✓
Stage 3: Run Tests ✓
Stage 4: Push to Registry ✓ (nếu branch main)
Stage 5: Deploy ✓ (nếu branch main)

Finished: SUCCESS
```

### ✅ Bước 9: Test Webhook (Tự động trigger)

```bash
# Push một thay đổi nhỏ lên Git
cd /home/admin1/Code/ocr_khai_sinh
echo "# Test CI/CD" >> README.md
git add README.md
git commit -m "Test Jenkins CI/CD"
git push origin main
```

**Jenkins sẽ tự động:**
1. Detect push event từ webhook
2. Checkout code mới
3. Chạy toàn bộ pipeline
4. Build → Test → Push → Deploy

### 🎉 Hoàn thành!

Từ giờ, mỗi khi bạn push code lên Git:
- ✅ Jenkins tự động detect
- ✅ Build Docker image
- ✅ Run tests
- ✅ Push lên Docker registry
- ✅ Deploy lên server (nếu branch main)

---

## 🐛 Troubleshooting

### Jenkins không detect webhook?

**Kiểm tra:**
```bash
# 1. Jenkins có thể truy cập từ internet không?
curl http://YOUR_JENKINS_IP:8080

# 2. Firewall có block port 8080 không?
sudo ufw status

# 3. Kiểm tra webhook logs trong GitHub/GitLab
```

**Giải pháp tạm thời:** Dùng Poll SCM thay vì webhook

### Build fail với "Cannot connect to Docker daemon"?

```bash
# Thêm Jenkins user vào docker group
docker exec -u root jenkins usermod -aG docker jenkins
docker restart jenkins
```

### Credentials không work?

- Kiểm tra ID credentials phải khớp với Jenkinsfile
- Test credentials bằng cách chạy manual build

---

## 📊 Monitoring

### Xem build history:
- Vào Jenkins job → **Build History**

### Xem logs:
```bash
# Jenkins logs
docker logs -f jenkins

# Application logs
docker-compose logs -f
```

### Email notifications (Optional):
1. **Manage Jenkins** → **Configure System**
2. **E-mail Notification**
3. Cấu hình SMTP server
4. Thêm vào Jenkinsfile:
```groovy
post {
    failure {
        mail to: 'your-email@example.com',
             subject: "Build Failed: ${env.JOB_NAME}",
             body: "Build failed. Check: ${env.BUILD_URL}"
    }
}
```
