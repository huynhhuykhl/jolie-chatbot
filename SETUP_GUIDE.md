# Hướng Dẫn Kết Nối Chatbot với Facebook Messenger

Tài liệu này hướng dẫn từng bước để kết nối chatbot AI của bạn với Facebook Fanpage.

## 📋 Yêu Cầu Trước Khi Bắt Đầu

- Một tài khoản Facebook (có quyền quản lý fanpage)
- Một fanpage Facebook
- Một máy chủ hoặc hosting (để chạy chatbot)
- OpenAI API key (để sử dụng AI)

---

## 🔑 Bước 1: Lấy Facebook Page Access Token

### 1.1 Truy cập Facebook Developers

1. Mở [https://developers.facebook.com](https://developers.facebook.com)
2. Đăng nhập bằng tài khoản Facebook của bạn
3. Nhấp vào "My Apps" (Ứng dụng của tôi)

### 1.2 Tạo Ứng Dụng Mới

1. Nhấp "Create App" (Tạo ứng dụng)
2. Chọn "Consumer" (Người tiêu dùng)
3. Điền thông tin:
   - **App Name**: "Facebook Chatbot" (hoặc tên khác)
   - **App Contact Email**: Email của bạn
   - **App Purpose**: Chọn "Business"
4. Nhấp "Create App"

### 1.3 Thêm Sản Phẩm Messenger

1. Trong dashboard ứng dụng, tìm "Messenger"
2. Nhấp "Set Up" (Thiết lập)
3. Chọn "Messenger" → "Set Up"

### 1.4 Lấy Page Access Token

1. Trong Messenger settings, tìm "Access Tokens"
2. Nhấp "Add or Remove Page" (Thêm hoặc xóa trang)
3. Chọn fanpage của bạn
4. Chấp nhận quyền
5. **Sao chép Page Access Token** (lưu ở đâu đó an toàn)

---

## 🔐 Bước 2: Tạo Verify Token

Verify Token là một chuỗi bất kỳ mà bạn chọn để xác minh webhook.

**Ví dụ:**
```
my_super_secret_verify_token_12345
```

Hãy tạo một chuỗi ngẫu nhiên và lưu lại.

---

## 🚀 Bước 3: Triển Khai Chatbot

### 3.1 Chuẩn Bị Môi Trường

```bash
# Clone hoặc tải chatbot code
cd /home/ubuntu/facebook-chatbot

# Cài đặt dependencies
pip install -r requirements.txt
```

### 3.2 Cấu Hình Biến Môi Trường

Tạo file `.env` từ `.env.example`:

```bash
cp .env.example .env
```

Chỉnh sửa file `.env` với thông tin của bạn:

```
FACEBOOK_PAGE_ACCESS_TOKEN=your_page_access_token_here
FACEBOOK_VERIFY_TOKEN=your_verify_token_here
OPENAI_API_KEY=your_openai_api_key_here
```

### 3.3 Chạy Chatbot Locally (Để Test)

```bash
python main.py
```

Chatbot sẽ chạy tại `http://localhost:8000`

---

## 🌐 Bước 4: Triển Khai Lên Server

Bạn có thể triển khai chatbot lên các nền tảng sau:

### Tùy Chọn 1: Heroku (Miễn Phí)

1. Tạo tài khoản [Heroku](https://www.heroku.com)
2. Cài đặt Heroku CLI
3. Tạo file `Procfile`:
   ```
   web: uvicorn main:app --host 0.0.0.0 --port $PORT
   ```
4. Deploy:
   ```bash
   heroku login
   heroku create your-chatbot-name
   git push heroku main
   heroku config:set FACEBOOK_PAGE_ACCESS_TOKEN=your_token
   heroku config:set FACEBOOK_VERIFY_TOKEN=your_token
   heroku config:set OPENAI_API_KEY=your_key
   ```

### Tùy Chọn 2: AWS, Google Cloud, Azure

Tương tự như Heroku, bạn có thể triển khai trên các nền tảng cloud khác.

### Tùy Chọn 3: VPS/Dedicated Server

```bash
# SSH vào server
ssh user@your_server_ip

# Clone code
git clone your_repo_url
cd facebook-chatbot

# Cài đặt dependencies
pip install -r requirements.txt

# Chạy với supervisor hoặc systemd
# (Xem phần Chạy Chatbot Liên Tục bên dưới)
```

---

## 🔗 Bước 5: Kết Nối Webhook với Facebook

### 5.1 Lấy URL Webhook

Sau khi triển khai, bạn sẽ có URL như:
```
https://your-domain.com/webhook
```

### 5.2 Thiết Lập Webhook trong Facebook Developers

1. Trở lại [Facebook Developers](https://developers.facebook.com)
2. Vào ứng dụng của bạn → Messenger → Settings
3. Tìm "Webhooks"
4. Nhấp "Add Callback URL" (Thêm URL Callback)
5. Điền thông tin:
   - **Callback URL**: `https://your-domain.com/webhook`
   - **Verify Token**: Nhập verify token bạn tạo ở Bước 2
6. Nhấp "Verify and Save"

### 5.3 Đăng Ký Webhook Events

1. Trong "Webhooks" settings
2. Tìm "Subscribe to this object"
3. Chọn các events:
   - ✅ `messages`
   - ✅ `messaging_postbacks`
   - ✅ `messaging_optins`
4. Nhấp "Save"

---

## 🧪 Bước 6: Kiểm Thử Chatbot

### 6.1 Test Webhook Locally

Nếu bạn chạy locally, bạn có thể sử dụng **ngrok** để expose URL:

```bash
# Cài đặt ngrok
# Từ https://ngrok.com/download

# Chạy ngrok
ngrok http 8000

# Sẽ hiển thị URL như:
# https://abc123.ngrok.io
```

Sau đó sử dụng URL ngrok trong Facebook Developers.

### 6.2 Test Trên Facebook

1. Mở fanpage của bạn
2. Nhấp "Send Message" (Gửi tin nhắn)
3. Gửi một tin nhắn test
4. Chatbot sẽ trả lời trong vài giây

---

## 🛠️ Chạy Chatbot Liên Tục (Production)

### Sử Dụng Supervisor

```bash
# Cài đặt supervisor
sudo apt-get install supervisor

# Tạo file cấu hình
sudo nano /etc/supervisor/conf.d/chatbot.conf
```

Nội dung file:
```ini
[program:facebook-chatbot]
directory=/home/ubuntu/facebook-chatbot
command=/usr/bin/python3 main.py
autostart=true
autorestart=true
stderr_logfile=/var/log/chatbot.err.log
stdout_logfile=/var/log/chatbot.out.log
environment=FACEBOOK_PAGE_ACCESS_TOKEN="your_token",FACEBOOK_VERIFY_TOKEN="your_token",OPENAI_API_KEY="your_key"
```

Khởi động:
```bash
sudo supervisorctl reread
sudo supervisorctl update
sudo supervisorctl start facebook-chatbot
```

### Sử Dụng Systemd

Tạo file `/etc/systemd/system/chatbot.service`:

```ini
[Unit]
Description=Facebook Messenger Chatbot
After=network.target

[Service]
Type=simple
User=ubuntu
WorkingDirectory=/home/ubuntu/facebook-chatbot
ExecStart=/usr/bin/python3 main.py
Restart=always
Environment="FACEBOOK_PAGE_ACCESS_TOKEN=your_token"
Environment="FACEBOOK_VERIFY_TOKEN=your_token"
Environment="OPENAI_API_KEY=your_key"

[Install]
WantedBy=multi-user.target
```

Khởi động:
```bash
sudo systemctl daemon-reload
sudo systemctl enable chatbot
sudo systemctl start chatbot
```

---

## 📊 Giám Sát Chatbot

### Kiểm Tra Logs

```bash
# Với supervisor
sudo tail -f /var/log/chatbot.out.log

# Với systemd
sudo journalctl -u chatbot -f
```

### Health Check

Truy cập:
```
https://your-domain.com/health
```

Bạn sẽ thấy:
```json
{
  "status": "healthy",
  "service": "Facebook Messenger Chatbot",
  "timestamp": "2024-01-15T10:30:00"
}
```

---

## 🎨 Tùy Chỉnh Chatbot

### Thay Đổi Hành Vi AI

Mở file `main.py` và tìm phần system prompt:

```python
"content": """Bạn là một trợ lý chatbot thân thiện cho fanpage Facebook. 
Hãy trả lời các câu hỏi một cách ngắn gọn, hữu ích và thân thiện.
..."""
```

Chỉnh sửa text này để thay đổi cách chatbot trả lời.

### Thêm Xử Lý Đặc Biệt

Bạn có thể thêm các hàm xử lý riêng cho các loại tin nhắn khác nhau.

---

## ❓ Troubleshooting

### Lỗi: "Invalid verify token"

- Kiểm tra xem verify token trong `.env` có khớp với Facebook Developers không
- Kiểm tra xem webhook URL có chính xác không

### Lỗi: "Webhook not responding"

- Kiểm tra xem server có chạy không: `curl https://your-domain.com/health`
- Kiểm tra firewall/security group settings
- Kiểm tra logs để xem lỗi cụ thể

### Chatbot không trả lời

- Kiểm tra xem OpenAI API key có hợp lệ không
- Kiểm tra xem account OpenAI có credit không
- Kiểm tra logs để xem lỗi từ OpenAI

### Tin nhắn bị delay

- Có thể do OpenAI API chậm
- Kiểm tra network latency
- Xem xét upgrade server resources

---

## 📞 Hỗ Trợ Thêm

- [Facebook Developers Documentation](https://developers.facebook.com/docs/messenger-platform)
- [OpenAI API Documentation](https://platform.openai.com/docs)
- [FastAPI Documentation](https://fastapi.tiangolo.com)

---

**Chúc mừng! Chatbot của bạn đã sẵn sàng! 🎉**
