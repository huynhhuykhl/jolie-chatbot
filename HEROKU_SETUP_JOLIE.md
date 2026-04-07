# 🚀 Hướng Dẫn Triển Khai Chatbot Lên Heroku - Nhà Hàng Tiệc Cưới Jolie

## 📋 Thông Tin Dự Án

- **Fanpage**: Nhà Hàng Tiệc Cưới Jolie
- **URL Fanpage**: https://www.facebook.com/profile.php?id=61565921244138
- **Verify Token**: `jolie_verify_token_2026`
- **OpenAI API Key**: Đã cấu hình sẵn ✅

## 🔑 Bước 1: Lấy Facebook Page Access Token

### 1.1 Truy cập Facebook Graph API Explorer

1. Mở: https://developers.facebook.com/tools/explorer
2. Đảm bảo bạn đã đăng nhập bằng tài khoản Facebook có quyền quản lý fanpage

### 1.2 Lấy User Access Token

1. Ở phía trên bên phải, nhấp vào dropdown (nơi hiển thị tên bạn)
2. Chọn "Get User Access Token"
3. Một cửa sổ popup sẽ xuất hiện
4. Chọn các quyền sau:
   - ✅ `pages_manage_metadata`
   - ✅ `pages_messaging`
   - ✅ `pages_read_engagement`
5. Nhấp "Generate Access Token"
6. **Sao chép token này** (lưu ở đâu đó tạm thời)

### 1.3 Lấy Page Access Token

1. Quay lại Graph API Explorer
2. Thay đổi dropdown từ "GET" sang "GET"
3. Trong ô input, nhập: `me/accounts`
4. Nhấp "Submit"
5. Kết quả sẽ hiển thị danh sách fanpage của bạn
6. Tìm fanpage "Nhà Hàng Tiệc Cưới Jolie" trong danh sách
7. **Sao chép giá trị `access_token` của fanpage này**

Ví dụ kết quả:
```json
{
  "data": [
    {
      "access_token": "EAABs...",  // ← Sao chép cái này
      "category": "Restaurant",
      "category_list": [...],
      "name": "Nhà Hàng Tiệc Cưới Jolie",
      "id": "61565921244138"
    }
  ]
}
```

---

## 🌐 Bước 2: Chuẩn Bị Heroku

### 2.1 Tạo Tài Khoản Heroku

1. Truy cập: https://www.heroku.com
2. Nhấp "Sign Up"
3. Điền thông tin và tạo tài khoản
4. Xác minh email

### 2.2 Cài Đặt Heroku CLI

**Trên Windows:**
- Tải từ: https://devcenter.heroku.com/articles/heroku-cli
- Chạy installer

**Trên Mac:**
```bash
brew tap heroku/brew && brew install heroku
```

**Trên Linux:**
```bash
curl https://cli-assets.heroku.com/install.sh | sh
```

### 2.3 Đăng Nhập Heroku

```bash
heroku login
```

Một trình duyệt sẽ mở ra, đăng nhập bằng tài khoản Heroku của bạn.

---

## 📦 Bước 3: Chuẩn Bị Code

### 3.1 Tải Code Chatbot

Bạn đã có code trong thư mục `facebook-chatbot`. Đảm bảo các file sau có mặt:
- `main.py`
- `requirements.txt`
- `Procfile`
- `.env` (đã được tạo sẵn)

### 3.2 Khởi Tạo Git Repository

```bash
cd facebook-chatbot
git init
git add .
git commit -m "Initial commit: Facebook chatbot for Jolie"
```

---

## 🚀 Bước 4: Deploy Lên Heroku

### 4.1 Tạo Ứng Dụng Heroku

```bash
heroku create jolie-chatbot
```

Bạn sẽ thấy:
```
Creating ⬢ jolie-chatbot... done
https://jolie-chatbot.herokuapp.com/ | https://git.heroku.com/jolie-chatbot.git
```

**Lưu URL này**: `https://jolie-chatbot.herokuapp.com`

### 4.2 Thiết Lập Biến Môi Trường

```bash
# Thiết lập Page Access Token (thay YOUR_PAGE_ACCESS_TOKEN bằng token bạn lấy ở Bước 1.3)
heroku config:set FACEBOOK_PAGE_ACCESS_TOKEN=YOUR_PAGE_ACCESS_TOKEN

# Verify Token (đã được cấu hình sẵn)
heroku config:set FACEBOOK_VERIFY_TOKEN=jolie_verify_token_2026

# OpenAI API Key (đã được cấu hình sẵn)
heroku config:set OPENAI_API_KEY=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
```

### 4.3 Deploy Code

```bash
git push heroku main
```

Hoặc nếu branch là `master`:
```bash
git push heroku master
```

Chờ quá trình deploy hoàn tất. Bạn sẽ thấy:
```
remote: -----> Building on the Heroku-20 stack
...
remote: -----> Launching... done
```

### 4.4 Kiểm Tra Ứng Dụng

```bash
# Xem logs
heroku logs --tail

# Hoặc truy cập health check
curl https://jolie-chatbot.herokuapp.com/health
```

Bạn sẽ thấy:
```json
{
  "status": "healthy",
  "service": "Facebook Messenger Chatbot",
  "timestamp": "2026-04-07T..."
}
```

---

## 🔗 Bước 5: Kết Nối Webhook với Facebook

### 5.1 Truy Cập Facebook Developers

1. Mở: https://developers.facebook.com/apps/931658612995239
2. Chọn "Messenger" từ menu bên trái
3. Tìm mục "Webhooks"

### 5.2 Thiết Lập Webhook

1. Nhấp "Add Callback URL" (hoặc "Edit Callback URL" nếu đã có)
2. Điền thông tin:
   - **Callback URL**: `https://jolie-chatbot.herokuapp.com/webhook`
   - **Verify Token**: `jolie_verify_token_2026`
3. Nhấp "Verify and Save"

### 5.3 Đăng Ký Webhook Events

1. Trong "Webhooks" settings
2. Tìm "Subscribe to this object"
3. Chọn các events:
   - ✅ `messages`
   - ✅ `messaging_postbacks`
4. Nhấp "Save"

---

## ✅ Bước 6: Kiểm Thử Chatbot

### 6.1 Test Trên Fanpage

1. Mở fanpage: https://www.facebook.com/profile.php?id=61565921244138
2. Nhấp "Send Message" (Gửi tin nhắn)
3. Gửi một tin nhắn test, ví dụ: "Xin chào"
4. Chatbot sẽ trả lời trong vài giây

### 6.2 Kiểm Tra Logs

```bash
heroku logs --tail
```

Bạn sẽ thấy các tin nhắn được xử lý:
```
INFO:     127.0.0.1:12345 - "POST /webhook HTTP/1.1" 200 OK
```

---

## 🎨 Tùy Chỉnh Chatbot

### Thay Đổi Hành Vi AI

Nếu bạn muốn chatbot trả lời theo cách khác, hãy:

1. Mở file `main.py`
2. Tìm hàm `get_ai_response()`
3. Chỉnh sửa system prompt:

```python
"content": """Bạn là một trợ lý chatbot cho Nhà Hàng Tiệc Cưới Jolie. 
Hãy trả lời các câu hỏi về nhà hàng, tiệc cưới, menu, giá cả, v.v.
Luôn thân thiện và hữu ích."""
```

4. Commit và push lên Heroku:
```bash
git add main.py
git commit -m "Update chatbot behavior"
git push heroku main
```

---

## 📊 Giám Sát Chatbot

### Xem Logs Real-time

```bash
heroku logs --tail
```

### Kiểm Tra Sức Khỏe

```bash
curl https://jolie-chatbot.herokuapp.com/health
```

### Khởi Động Lại

```bash
heroku restart
```

---

## ⚙️ Cấu Hình Nâng Cao

### Tăng Giới Hạn Dyno

Heroku free tier có giới hạn. Nếu cần tăng performance:

```bash
heroku ps:scale web=1:standard-1x
```

(Lưu ý: Điều này sẽ tính phí)

### Xem Tất Cả Cấu Hình

```bash
heroku config
```

### Thay Đổi Cấu Hình

```bash
heroku config:set FACEBOOK_PAGE_ACCESS_TOKEN=new_token
```

---

## ❓ Troubleshooting

### Lỗi: "Invalid verify token"
- Kiểm tra xem verify token trong Heroku config có khớp với Facebook Developers không
- Chạy: `heroku config` để kiểm tra

### Lỗi: "Webhook not responding"
- Kiểm tra logs: `heroku logs --tail`
- Đảm bảo URL callback đúng: `https://jolie-chatbot.herokuapp.com/webhook`

### Chatbot không trả lời
- Kiểm tra OpenAI API key có hợp lệ không
- Xem logs để tìm lỗi cụ thể

### Heroku dyno ngủ (Free tier)
- Free tier sẽ ngủ sau 30 phút không hoạt động
- Để tránh, upgrade lên paid tier hoặc sử dụng uptime monitor

---

## 🎉 Hoàn Thành!

Chatbot của bạn đã được triển khai thành công lên Heroku! 

**Tóm tắt:**
- ✅ Fanpage: Nhà Hàng Tiệc Cưới Jolie
- ✅ Webhook URL: `https://jolie-chatbot.herokuapp.com/webhook`
- ✅ Verify Token: `jolie_verify_token_2026`
- ✅ AI: OpenAI GPT-4.1-mini
- ✅ Ngôn ngữ: Tiếng Việt

---

## 📞 Hỗ Trợ

Nếu bạn gặp vấn đề:
1. Kiểm tra logs: `heroku logs --tail`
2. Xem file SETUP_GUIDE.md để hướng dẫn chi tiết
3. Kiểm tra kết nối mạng

---

**Tạo bởi:** Manus AI Assistant  
**Ngày tạo:** 2026-04-07  
**Phiên bản:** 1.0
