# 🚀 Quick Start - Bắt Đầu Nhanh

Hướng dẫn này giúp bạn bắt đầu trong 5 phút!

## ⚡ 5 Bước Nhanh

### Bước 1: Chuẩn Bị Thông Tin (2 phút)

Bạn cần có:
- **Facebook Page Access Token** - [Hướng dẫn lấy](SETUP_GUIDE.md#14-lấy-page-access-token)
- **Verify Token** - Một chuỗi bất kỳ, ví dụ: `my_verify_token_123`
- **OpenAI API Key** - [Lấy từ đây](https://platform.openai.com/api-keys)

### Bước 2: Cài Đặt (1 phút)

```bash
# Cài đặt dependencies
pip install -r requirements.txt

# Tạo file .env
cp .env.example .env
```

### Bước 3: Cấu Hình (1 phút)

Chỉnh sửa file `.env`:

```bash
nano .env
```

Điền thông tin:
```
FACEBOOK_PAGE_ACCESS_TOKEN=your_page_access_token_here
FACEBOOK_VERIFY_TOKEN=your_verify_token_here
OPENAI_API_KEY=your_openai_api_key_here
```

Lưu: `Ctrl+O`, `Enter`, `Ctrl+X`

### Bước 4: Chạy Chatbot (1 phút)

```bash
python main.py
```

Bạn sẽ thấy:
```
INFO:     Uvicorn running on http://0.0.0.0:8000
```

### Bước 5: Kết Nối với Facebook (Vài phút)

#### 5.1 Nếu chạy locally, sử dụng ngrok:

```bash
# Cài đặt ngrok từ https://ngrok.com/download

# Chạy ngrok
ngrok http 8000

# Sẽ hiển thị: https://abc123.ngrok.io
```

#### 5.2 Trong Facebook Developers:

1. Vào [Facebook Developers](https://developers.facebook.com)
2. Chọn ứng dụng của bạn
3. Messenger → Settings
4. Tìm "Webhooks"
5. Nhấp "Add Callback URL"
6. Điền:
   - **Callback URL**: `https://abc123.ngrok.io/webhook` (hoặc domain của bạn)
   - **Verify Token**: Nhập verify token từ `.env`
7. Nhấp "Verify and Save"

#### 5.3 Đăng ký events:

1. Trong "Webhooks" settings
2. Tìm "Subscribe to this object"
3. Chọn: `messages` và `messaging_postbacks`
4. Nhấp "Save"

## ✅ Kiểm Tra

Mở fanpage của bạn và gửi một tin nhắn. Chatbot sẽ trả lời trong vài giây!

## 📚 Tiếp Theo

- **Triển khai lên server**: Xem [DEPLOYMENT_VPS.md](DEPLOYMENT_VPS.md)
- **Hướng dẫn chi tiết**: Xem [SETUP_GUIDE.md](SETUP_GUIDE.md)
- **Tùy chỉnh chatbot**: Xem [README.md](README.md#-tùy-chỉnh)

## ❓ Gặp Vấn Đề?

### Lỗi: "Invalid verify token"
- Kiểm tra xem verify token trong `.env` có khớp với Facebook Developers không

### Lỗi: "Webhook not responding"
- Kiểm tra xem ngrok hoặc server có chạy không
- Kiểm tra xem URL callback có chính xác không

### Chatbot không trả lời
- Kiểm tra xem OpenAI API key có hợp lệ không
- Xem logs: `tail -f /var/log/chatbot.out.log`

---

**Bạn đã sẵn sàng! Hãy tạo chatbot AI tuyệt vời cho fanpage của mình! 🎉**
