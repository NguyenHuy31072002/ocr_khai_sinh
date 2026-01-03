# 🔗 Cấu hình GitHub Webhook cho Jenkins

## ⚠️ VẤN ĐỀ QUAN TRỌNG

Webhook chỉ hoạt động nếu **GitHub có thể truy cập được Jenkins server của bạn**.

### Tình huống của bạn:

- **Jenkins IP**: `192.168.1.19:8080` (Local network)
- **GitHub**: Trên internet, không thể truy cập IP local của bạn

## 🎯 GIẢI PHÁP

### Option 1: Sử dụng Poll SCM (KHUYẾN NGHỊ cho local development)

**Không cần webhook**, Jenkins tự động kiểm tra Git mỗi vài phút.

#### Cách setup:

1. Vào Jenkins job → **Configure**
2. **Build Triggers** section:
   - ✅ Chọn **Poll SCM**
   - **Schedule**: `H/5 * * * *` (kiểm tra mỗi 5 phút)
3. **Save**

**Ưu điểm:**
- ✅ Không cần public IP
- ✅ Hoạt động với Jenkins local
- ✅ Đơn giản, dễ setup

**Nhược điểm:**
- ⏱️ Delay 5 phút (không real-time)

---

### Option 2: Expose Jenkins ra Internet (Cho production)

Nếu muốn webhook real-time, cần expose Jenkins:

#### A. Sử dụng ngrok (Tạm thời, cho test)

```bash
# Cài ngrok
wget https://bin.equinox.io/c/bNyj1mQVY4c/ngrok-v3-stable-linux-amd64.tgz
tar xvzf ngrok-v3-stable-linux-amd64.tgz
sudo mv ngrok /usr/local/bin/

# Chạy ngrok
ngrok http 8080
```

Ngrok sẽ cho bạn URL public, ví dụ: `https://abc123.ngrok.io`

**Payload URL trong GitHub webhook:**
```
https://abc123.ngrok.io/github-webhook/
```

#### B. Sử dụng Public IP + Port Forwarding (Production)

1. Cấu hình port forwarding trên router: `8080 → 192.168.1.19:8080`
2. Lấy public IP: `curl ifconfig.me`
3. **Payload URL**: `http://YOUR_PUBLIC_IP:8080/github-webhook/`

⚠️ **Lưu ý bảo mật:** Nên dùng HTTPS và authentication

---

### Option 3: Deploy Jenkins lên Cloud (Tốt nhất cho production)

Deploy Jenkins lên:
- AWS EC2
- Google Cloud
- DigitalOcean
- Azure

Sau đó dùng public URL của cloud server.

---

## 🚀 KHUYẾN NGHỊ CHO BẠN

**Vì bạn đang develop local**, tôi khuyên dùng **Option 1: Poll SCM**

### Cách setup Poll SCM:

1. **Bỏ qua webhook** trong GitHub (không cần thêm)
2. Vào Jenkins job → **Configure**
3. **Build Triggers**:
   - ✅ **Poll SCM**
   - **Schedule**: `H/5 * * * *`
4. **Save**

Từ giờ, mỗi 5 phút Jenkins sẽ tự kiểm tra Git. Nếu có thay đổi → tự động build!

### Test:
```bash
# Push code
git add .
git commit -m "Test Jenkins polling"
git push origin main

# Đợi tối đa 5 phút, Jenkins sẽ tự động build
```

---

## 📊 So sánh các Options

| Option | Real-time | Phức tạp | Phù hợp |
|--------|-----------|----------|---------|
| Poll SCM | ❌ (delay 5 phút) | ⭐ Dễ | ✅ Local dev |
| ngrok | ✅ | ⭐⭐ Trung bình | Test webhook |
| Public IP | ✅ | ⭐⭐⭐ Khó | Production |
| Cloud | ✅ | ⭐⭐⭐⭐ Rất khó | Production |

---

## 🎯 HÀNH ĐỘNG TIẾP THEO

**Bạn muốn làm gì?**

**A. Dùng Poll SCM (Đơn giản nhất)**
→ Không cần webhook, Jenkins tự check Git mỗi 5 phút

**B. Test webhook với ngrok**
→ Cài ngrok để có public URL

**C. Để sau, focus vào test pipeline trước**
→ Chạy manual build trong Jenkins để test

Bạn chọn cái nào? 😊
