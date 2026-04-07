# Facebook Messenger Chatbot with AI

Một chatbot AI thông minh tích hợp với Facebook Messenger, được xây dựng bằng FastAPI và OpenAI.

## ✨ Tính Năng

- 🤖 **AI Thông Minh**: Sử dụng OpenAI GPT-4 để trả lời câu hỏi tự nhiên
- 💬 **Hỗ Trợ Tiếng Việt**: Trả lời hoàn toàn bằng tiếng Việt
- 📝 **Lịch Sử Trò Chuyện**: Nhớ lại các cuộc trò chuyện trước đó với mỗi user
- ⚡ **Nhanh Chóng**: Phản hồi trong vài giây
- 🔒 **An Toàn**: Xác minh webhook với Facebook
- 📊 **Logging**: Ghi lại tất cả các tin nhắn để phân tích
- 🚀 **Dễ Triển Khai**: Hỗ trợ Docker, Heroku, VPS

## 📋 Yêu Cầu

- Python 3.8+
- Facebook Fanpage
- OpenAI API Key
- Máy chủ/Hosting (để chạy chatbot)

## 🚀 Cài Đặt Nhanh

### 1. Clone hoặc tải code

```bash
cd facebook-chatbot
```

### 2. Cài đặt dependencies

```bash
pip install -r requirements.txt
```

### 3. Cấu hình biến môi trường

```bash
cp .env.example .env
# Chỉnh sửa .env với thông tin của bạn
```

### 4. Chạy chatbot

```bash
python main.py
```

Chatbot sẽ chạy tại `http://localhost:8000`

## 📖 Hướng Dẫn Chi Tiết

Xem file [SETUP_GUIDE.md](./SETUP_GUIDE.md) để hướng dẫn đầy đủ về:

- Cách lấy Facebook Page Access Token
- Cách tạo Verify Token
- Cách triển khai lên server
- Cách kết nối webhook với Facebook
- Cách kiểm thử chatbot
- Cách chạy chatbot liên tục

## 🐳 Triển Khai với Docker

```bash
# Build image
docker build -t facebook-chatbot .

# Chạy container
docker run -e FACEBOOK_PAGE_ACCESS_TOKEN=your_token \
           -e FACEBOOK_VERIFY_TOKEN=your_token \
           -e OPENAI_API_KEY=your_key \
           -p 8000:8000 \
           facebook-chatbot
```

Hoặc sử dụng docker-compose:

```bash
docker-compose up -d
```

## 🌐 Triển Khai lên Heroku

```bash
# Cài đặt Heroku CLI
# Từ https://devcenter.heroku.com/articles/heroku-cli

# Login
heroku login

# Tạo app
heroku create your-chatbot-name

# Thiết lập biến môi trường
heroku config:set FACEBOOK_PAGE_ACCESS_TOKEN=your_token
heroku config:set FACEBOOK_VERIFY_TOKEN=your_token
heroku config:set OPENAI_API_KEY=your_key

# Deploy
git push heroku main
```

## 📁 Cấu Trúc Dự Án

```
facebook-chatbot/
├── main.py                 # Ứng dụng chính
├── requirements.txt        # Python dependencies
├── .env.example           # Ví dụ biến môi trường
├── Dockerfile             # Docker configuration
├── docker-compose.yml     # Docker Compose configuration
├── Procfile              # Heroku configuration
├── SETUP_GUIDE.md        # Hướng dẫn chi tiết
└── README.md             # File này
```

## 🔌 API Endpoints

### GET /webhook
Xác minh webhook với Facebook

**Query Parameters:**
- `hub.mode`: "subscribe"
- `hub.verify_token`: Verify token của bạn
- `hub.challenge`: Challenge string

**Response:**
```
Challenge string
```

### POST /webhook
Nhận và xử lý tin nhắn từ Facebook

**Request Body:**
```json
{
  "object": "page",
  "entry": [
    {
      "messaging": [
        {
          "sender": {"id": "user_id"},
          "recipient": {"id": "page_id"},
          "message": {"text": "Hello"}
        }
      ]
    }
  ]
}
```

**Response:**
```json
{"status": "ok"}
```

### GET /
Health check endpoint

**Response:**
```json
{
  "status": "running",
  "service": "Facebook Messenger Chatbot",
  "timestamp": "2024-01-15T10:30:00"
}
```

### GET /health
Kiểm tra sức khỏe dịch vụ

**Response:**
```json
{
  "status": "healthy",
  "service": "Facebook Messenger Chatbot",
  "timestamp": "2024-01-15T10:30:00"
}
```

## 🎨 Tùy Chỉnh

### Thay Đổi Hành Vi AI

Mở `main.py` và tìm hàm `get_ai_response()`. Chỉnh sửa system prompt:

```python
"content": """Bạn là một trợ lý chatbot thân thiện cho fanpage Facebook. 
Hãy trả lời các câu hỏi một cách ngắn gọn, hữu ích và thân thiện."""
```

### Thêm Xử Lý Đặc Biệt

Bạn có thể thêm các hàm xử lý riêng cho các loại tin nhắn khác nhau trong hàm `handle_webhook()`.

## 📊 Giám Sát

### Logs

Chatbot ghi lại tất cả các tin nhắn và lỗi. Xem logs:

```bash
# Nếu chạy locally
# Logs sẽ hiển thị trực tiếp trên console

# Nếu chạy với Docker
docker logs -f container_name

# Nếu chạy với Heroku
heroku logs --tail
```

### Health Check

```bash
curl https://your-domain.com/health
```

## ❓ Troubleshooting

### Lỗi: "Invalid verify token"
- Kiểm tra xem verify token trong `.env` có khớp với Facebook Developers không

### Lỗi: "Webhook not responding"
- Kiểm tra xem server có chạy không: `curl https://your-domain.com/health`
- Kiểm tra firewall settings

### Chatbot không trả lời
- Kiểm tra xem OpenAI API key có hợp lệ không
- Kiểm tra xem account OpenAI có credit không

## 📚 Tài Liệu Tham Khảo

- [Facebook Developers - Messenger Platform](https://developers.facebook.com/docs/messenger-platform)
- [OpenAI API Documentation](https://platform.openai.com/docs)
- [FastAPI Documentation](https://fastapi.tiangolo.com)
- [Python Requests Library](https://requests.readthedocs.io)

## 📝 License

MIT License

## 👨‍💻 Tác Giả

Tạo bởi Manus AI Assistant

## 📞 Hỗ Trợ

Nếu bạn gặp vấn đề, vui lòng:
1. Kiểm tra file [SETUP_GUIDE.md](./SETUP_GUIDE.md)
2. Xem logs để tìm lỗi cụ thể
3. Kiểm tra các tài liệu tham khảo ở trên

---

**Chúc mừng! Bạn đã sẵn sàng để tạo chatbot AI cho fanpage của mình! 🎉**
