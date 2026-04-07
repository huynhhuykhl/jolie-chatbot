# 📦 Tóm Tắt Dự Án Chatbot Facebook

## 🎯 Mục Tiêu

Xây dựng một chatbot AI thông minh tích hợp với Facebook Messenger, có khả năng trả lời câu hỏi tự nhiên bằng tiếng Việt.

## ✅ Những Gì Đã Hoàn Thành

### 1. Backend Chatbot (main.py)
- ✅ FastAPI server chạy trên port 8000
- ✅ Webhook endpoint để nhận tin nhắn từ Facebook
- ✅ Tích hợp OpenAI API (GPT-4.1-mini)
- ✅ Lưu trữ lịch sử trò chuyện cho mỗi user
- ✅ Xử lý tin nhắn text từ Facebook Messenger
- ✅ Gửi phản hồi AI về Facebook
- ✅ Health check endpoints
- ✅ Logging đầy đủ

### 2. Cấu Hình & Dependencies
- ✅ requirements.txt - Danh sách dependencies Python
- ✅ .env.example - Template cấu hình
- ✅ Dockerfile - Containerize ứng dụng
- ✅ docker-compose.yml - Dễ triển khai
- ✅ Procfile - Hỗ trợ Heroku

### 3. Hướng Dẫn & Tài Liệu
- ✅ **QUICK_START.md** - Bắt đầu nhanh trong 5 phút
- ✅ **SETUP_GUIDE.md** - Hướng dẫn chi tiết đầy đủ
- ✅ **DEPLOYMENT_VPS.md** - Triển khai lên VPS
- ✅ **README.md** - Tổng quan dự án
- ✅ **PROJECT_SUMMARY.md** - File này

### 4. Testing & Debugging
- ✅ test_webhook.py - Script kiểm thử webhook
- ✅ Health check endpoint
- ✅ Logging chi tiết

## 📁 Cấu Trúc Dự Án

```
facebook-chatbot/
├── main.py                    # Ứng dụng chính (FastAPI + OpenAI)
├── requirements.txt           # Python dependencies
├── .env.example              # Template biến môi trường
├── Dockerfile                # Docker configuration
├── docker-compose.yml        # Docker Compose setup
├── Procfile                  # Heroku deployment
├── test_webhook.py           # Script kiểm thử
│
├── QUICK_START.md            # 🚀 Bắt đầu nhanh (5 phút)
├── SETUP_GUIDE.md            # 📖 Hướng dẫn chi tiết
├── DEPLOYMENT_VPS.md         # 🌐 Triển khai VPS
├── README.md                 # 📚 Tài liệu chính
└── PROJECT_SUMMARY.md        # 📦 File này
```

## 🔑 Tính Năng Chính

| Tính Năng | Mô Tả |
|-----------|-------|
| **AI Thông Minh** | Sử dụng OpenAI GPT-4.1-mini để trả lời tự nhiên |
| **Tiếng Việt** | Trả lời hoàn toàn bằng tiếng Việt |
| **Lịch Sử Trò Chuyện** | Nhớ lại các cuộc trò chuyện trước đó |
| **Webhook Verification** | Xác minh webhook với Facebook |
| **Logging** | Ghi lại tất cả tin nhắn và lỗi |
| **Health Check** | Kiểm tra sức khỏe dịch vụ |
| **Docker Support** | Dễ triển khai với Docker |
| **Multiple Deployment** | Hỗ trợ Heroku, VPS, AWS, GCP, Azure |

## 🚀 Cách Sử Dụng

### Bước 1: Chuẩn Bị
```bash
# Cài đặt dependencies
pip install -r requirements.txt

# Tạo file .env
cp .env.example .env

# Chỉnh sửa .env với thông tin của bạn
nano .env
```

### Bước 2: Chạy Locally
```bash
python main.py
```

### Bước 3: Kết Nối với Facebook
1. Lấy Facebook Page Access Token
2. Tạo Verify Token
3. Thiết lập webhook URL trong Facebook Developers
4. Đăng ký webhook events

### Bước 4: Triển Khai Lên Server
- **Heroku**: Xem SETUP_GUIDE.md
- **VPS**: Xem DEPLOYMENT_VPS.md
- **Docker**: `docker-compose up -d`

## 📊 API Endpoints

| Endpoint | Phương Thức | Mô Tả |
|----------|------------|-------|
| `/webhook` | GET | Xác minh webhook với Facebook |
| `/webhook` | POST | Nhận và xử lý tin nhắn |
| `/health` | GET | Kiểm tra sức khỏe dịch vụ |
| `/` | GET | Health check cơ bản |

## 🔐 Biến Môi Trường

```
FACEBOOK_PAGE_ACCESS_TOKEN    # Token truy cập fanpage
FACEBOOK_VERIFY_TOKEN         # Token xác minh webhook
OPENAI_API_KEY               # API key OpenAI
```

## 📝 Quy Trình Hoạt Động

```
User gửi tin nhắn trên Facebook
           ↓
Facebook gửi webhook đến /webhook endpoint
           ↓
Chatbot nhận tin nhắn
           ↓
Lưu tin nhắn vào lịch sử trò chuyện
           ↓
Gọi OpenAI API để lấy phản hồi
           ↓
Lưu phản hồi vào lịch sử
           ↓
Gửi phản hồi về Facebook Messenger
           ↓
User nhận phản hồi từ chatbot
```

## 🧪 Kiểm Thử

### Test Webhook Locally
```bash
python test_webhook.py
```

### Test Health Check
```bash
curl http://localhost:8000/health
```

### Test với ngrok (Localhost)
```bash
ngrok http 8000
# Sử dụng URL ngrok trong Facebook Developers
```

## 🎨 Tùy Chỉnh

### Thay Đổi Hành Vi AI
Mở `main.py` và chỉnh sửa system prompt trong hàm `get_ai_response()`:

```python
"content": """Bạn là một trợ lý chatbot thân thiện cho fanpage Facebook. 
Hãy trả lời các câu hỏi một cách ngắn gọn, hữu ích và thân thiện."""
```

### Thêm Xử Lý Đặc Biệt
Bạn có thể thêm các hàm xử lý riêng cho các loại tin nhắn khác nhau.

## 📚 Tài Liệu Tham Khảo

- [Facebook Developers - Messenger Platform](https://developers.facebook.com/docs/messenger-platform)
- [OpenAI API Documentation](https://platform.openai.com/docs)
- [FastAPI Documentation](https://fastapi.tiangolo.com)
- [Python Requests Library](https://requests.readthedocs.io)

## ⚙️ Yêu Cầu Hệ Thống

| Yêu Cầu | Phiên Bản |
|---------|----------|
| Python | 3.8+ |
| FastAPI | 0.104.1+ |
| OpenAI | 1.3.0+ |
| Requests | 2.31.0+ |

## 🔄 Triển Khai

### Heroku
```bash
heroku create your-chatbot-name
git push heroku main
heroku config:set FACEBOOK_PAGE_ACCESS_TOKEN=...
```

### Docker
```bash
docker build -t chatbot .
docker run -e FACEBOOK_PAGE_ACCESS_TOKEN=... -p 8000:8000 chatbot
```

### VPS (Ubuntu)
```bash
# Xem DEPLOYMENT_VPS.md để hướng dẫn chi tiết
```

## 📞 Hỗ Trợ

Nếu bạn gặp vấn đề:
1. Kiểm tra file hướng dẫn tương ứng
2. Xem logs: `tail -f /var/log/chatbot.out.log`
3. Kiểm tra cấu hình biến môi trường
4. Kiểm tra kết nối mạng

## 📋 Danh Sách Kiểm Tra Triển Khai

- [ ] Lấy Facebook Page Access Token
- [ ] Tạo Verify Token
- [ ] Cấu hình file .env
- [ ] Cài đặt dependencies
- [ ] Chạy test webhook locally
- [ ] Triển khai lên server
- [ ] Cấu hình Nginx (nếu dùng VPS)
- [ ] Cấu hình SSL/HTTPS
- [ ] Kết nối webhook với Facebook
- [ ] Kiểm thử trên fanpage
- [ ] Giám sát logs

## 🎉 Kết Luận

Bạn đã có một chatbot AI hoàn chỉnh sẵn sàng để triển khai! Hãy làm theo các hướng dẫn để kết nối với fanpage Facebook của bạn.

---

**Tạo bởi:** Manus AI Assistant  
**Ngày tạo:** 2026-04-07  
**Phiên bản:** 1.0
