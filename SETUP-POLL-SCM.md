# ⏰ Setup Jenkins Poll SCM - Hướng dẫn từng bước

## Bạn vừa push code lên GitHub!

Commit: `9b47a07` - "huynk"
Files: 35 files changed, 1809 insertions(+)

## ⚠️ HIỆN TẠI: Jenkins CHƯA tự động build

Vì bạn chưa cấu hình Poll SCM hoặc webhook.

---

## ✅ SETUP POLL SCM - 5 BƯỚC

### Bước 1: Mở Jenkins
```
http://localhost:8080
```

### Bước 2: Vào Pipeline Job
- Click vào job: `ocr-khai-sinh-pipeline`
- Click **Configure** (bên trái)

### Bước 3: Tìm "Build Triggers"
- Scroll xuống phần **Build Triggers**

### Bước 4: Cấu hình Poll SCM
- ✅ Tick vào **Poll SCM**
- Trong ô **Schedule**, nhập:
  ```
  H/5 * * * *
  ```
  (Nghĩa là: kiểm tra Git mỗi 5 phút)

### Bước 5: Save
- Click **Save** ở cuối trang

---

## 🎉 SAU KHI SETUP

Jenkins sẽ:
1. Mỗi 5 phút kiểm tra Git
2. Nếu có commit mới → Tự động build
3. Bạn sẽ thấy build history trong Jenkins

---

## 🚀 HOẶC: Build ngay không cần đợi

Nếu không muốn đợi 5 phút

1. Vào Jenkins job
2. Click **Build Now**
3. Jenkins sẽ build ngay lập tức!

---

## 📊 Kiểm tra Build

Sau khi build (tự động hoặc manual):

1. Vào **Build History** (bên trái)
2. Click vào build number (ví dụ: #1, #2)
3. Click **Console Output** để xem logs

**Nếu thành công, bạn sẽ thấy:**
```
Stage 1: Checkout ✓
Stage 2: Build Docker Image ✓
Stage 3: Run Tests ✓
Stage 4: Push to Registry ✓
Stage 5: Deploy ✓

Finished: SUCCESS
```

---

## ⏱️ Timeline

```
Bây giờ (20:19)
  ↓
  Push code lên Git ✓
  ↓
  Setup Poll SCM trong Jenkins (làm ngay)
  ↓
  Đợi tối đa 5 phút
  ↓
  Jenkins tự động build!
```

---

## 🎯 KHUYẾN NGHỊ

**Làm ngay:**
1. Setup Poll SCM (5 phút)
2. Click "Build Now" để test ngay (không cần đợi)
3. Xem Console Output để verify

**Sau đó:**
- Mỗi lần push code → Đợi tối đa 5 phút → Jenkins tự build
