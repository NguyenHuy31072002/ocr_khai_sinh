#!/bin/bash

echo "=========================================="
echo "🎯 QUICK SETUP - Jenkins CI/CD"
echo "=========================================="
echo ""
echo "Repository: https://github.com/NguyenHuy31072002/ocr_khai_sinh.git"
echo ""

echo "📋 CHECKLIST - Làm theo thứ tự:"
echo ""
echo "☐ 1. Cài Jenkins:"
echo "     docker run -d --name jenkins -p 8080:8080 \\"
echo "       -v jenkins_home:/var/jenkins_home \\"
echo "       -v /var/run/docker.sock:/var/run/docker.sock \\"
echo "       --user root jenkins/jenkins:lts"
echo ""

echo "☐ 2. Truy cập Jenkins:"
echo "     URL: http://localhost:8080"
echo "     Password: docker exec jenkins cat /var/jenkins_home/secrets/initialAdminPassword"
echo ""

echo "☐ 3. Cài plugins:"
echo "     - Docker Pipeline"
echo "     - Git (đã có sẵn)"
echo "     - GitHub Integration"
echo ""

echo "☐ 4. Tạo Credentials (Manage Jenkins → Credentials):"
echo "     - docker-hub-credentials (Docker Hub login)"
echo "     - docker-registry-url (docker.io)"
echo "     - git-credentials (nếu repo private)"
echo ""

echo "☐ 5. Tạo Pipeline Job:"
echo "     - New Item → Pipeline"
echo "     - Name: ocr-khai-sinh-pipeline"
echo ""

echo "☐ 6. Cấu hình Pipeline:"
echo "     - SCM: Git"
echo "     - Repository: https://github.com/NguyenHuy31072002/ocr_khai_sinh.git"
echo "     - Branch: */main"
echo "     - Script Path: Jenkinsfile"
echo ""

echo "☐ 7. Cấu hình Webhook (GitHub):"
echo "     - Repo Settings → Webhooks → Add webhook"
echo "     - URL: http://YOUR_IP:8080/github-webhook/"
echo "     - Content type: application/json"
echo "     - Events: Push events"
echo ""

echo "☐ 8. Test Build:"
echo "     - Click 'Build Now' trong Jenkins"
echo "     - Xem Console Output"
echo ""

echo "☐ 9. Test Auto-trigger:"
echo "     - Push code lên GitHub"
echo "     - Jenkins sẽ tự động chạy!"
echo ""

echo "=========================================="
echo "📚 Chi tiết xem: SETUP-JENKINS-FROM-GIT.md"
echo "=========================================="
echo ""

read -p "Bạn muốn cài Jenkins ngay không? (y/n): " answer
if [ "$answer" = "y" ]; then
    echo ""
    echo "🚀 Đang cài Jenkins..."
    docker run -d \
      --name jenkins \
      -p 8080:8080 \
      -p 50000:50000 \
      -v jenkins_home:/var/jenkins_home \
      -v /var/run/docker.sock:/var/run/docker.sock \
      --user root \
      jenkins/jenkins:lts
    
    echo ""
    echo "✅ Jenkins đang khởi động..."
    echo "Đợi 30 giây..."
    sleep 30
    
    echo ""
    echo "🔑 Initial Admin Password:"
    docker exec jenkins cat /var/jenkins_home/secrets/initialAdminPassword
    
    echo ""
    echo "🌐 Mở browser: http://localhost:8080"
    echo ""
else
    echo ""
    echo "OK, bạn có thể chạy lại script này bất cứ lúc nào!"
    echo ""
fi
