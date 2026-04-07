# Hướng Dẫn Triển Khai Chatbot Lên VPS

Tài liệu này hướng dẫn triển khai chatbot lên một VPS (Virtual Private Server) như DigitalOcean, Linode, hay AWS EC2.

## 📋 Yêu Cầu

- Một VPS chạy Ubuntu 20.04 hoặc mới hơn
- SSH access đến VPS
- Domain hoặc subdomain (để sử dụng HTTPS)
- SSL certificate (từ Let's Encrypt - miễn phí)

## 🚀 Bước 1: Chuẩn Bị VPS

### 1.1 SSH vào VPS

```bash
ssh root@your_vps_ip
```

### 1.2 Cập nhật hệ thống

```bash
apt-get update
apt-get upgrade -y
```

### 1.3 Cài đặt các công cụ cần thiết

```bash
apt-get install -y \
    python3.11 \
    python3-pip \
    git \
    curl \
    wget \
    supervisor \
    nginx \
    certbot \
    python3-certbot-nginx
```

## 📥 Bước 2: Tải Code Chatbot

### 2.1 Clone repository

```bash
cd /home
git clone your_repo_url facebook-chatbot
cd facebook-chatbot
```

Hoặc nếu không có git, tải file:

```bash
cd /home
wget your_zip_url -O chatbot.zip
unzip chatbot.zip
cd facebook-chatbot
```

### 2.2 Cài đặt Python dependencies

```bash
pip3 install -r requirements.txt
```

## 🔐 Bước 3: Cấu Hình Biến Môi Trường

### 3.1 Tạo file .env

```bash
nano .env
```

Nội dung:
```
FACEBOOK_PAGE_ACCESS_TOKEN=your_page_access_token
FACEBOOK_VERIFY_TOKEN=your_verify_token
OPENAI_API_KEY=your_openai_api_key
```

Lưu file: `Ctrl+O`, `Enter`, `Ctrl+X`

### 3.2 Kiểm tra quyền

```bash
chmod 600 .env
```

## 🔄 Bước 4: Cấu Hình Supervisor (Chạy Chatbot Liên Tục)

### 4.1 Tạo file cấu hình supervisor

```bash
sudo nano /etc/supervisor/conf.d/chatbot.conf
```

Nội dung:
```ini
[program:facebook-chatbot]
directory=/home/facebook-chatbot
command=/usr/bin/python3 /home/facebook-chatbot/main.py
autostart=true
autorestart=true
stderr_logfile=/var/log/chatbot.err.log
stdout_logfile=/var/log/chatbot.out.log
user=root
environment=FACEBOOK_PAGE_ACCESS_TOKEN="your_token",FACEBOOK_VERIFY_TOKEN="your_token",OPENAI_API_KEY="your_key"
```

**Lưu ý:** Thay thế `your_token` và `your_key` bằng giá trị thực tế.

### 4.2 Khởi động supervisor

```bash
sudo supervisorctl reread
sudo supervisorctl update
sudo supervisorctl start facebook-chatbot
```

### 4.3 Kiểm tra trạng thái

```bash
sudo supervisorctl status facebook-chatbot
```

Bạn sẽ thấy:
```
facebook-chatbot                 RUNNING   pid 1234, uptime 0:00:10
```

## 🌐 Bước 5: Cấu Hình Nginx (Reverse Proxy)

### 5.1 Tạo file cấu hình Nginx

```bash
sudo nano /etc/nginx/sites-available/chatbot
```

Nội dung (thay `your-domain.com` bằng domain thực tế):
```nginx
server {
    listen 80;
    server_name your-domain.com www.your-domain.com;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

### 5.2 Kích hoạt site

```bash
sudo ln -s /etc/nginx/sites-available/chatbot /etc/nginx/sites-enabled/
```

### 5.3 Kiểm tra cấu hình Nginx

```bash
sudo nginx -t
```

Bạn sẽ thấy:
```
nginx: the configuration file /etc/nginx/nginx.conf syntax is ok
nginx: configuration file /etc/nginx/nginx.conf test is successful
```

### 5.4 Khởi động Nginx

```bash
sudo systemctl restart nginx
```

## 🔒 Bước 6: Cấu Hình SSL (HTTPS)

### 6.1 Lấy SSL certificate từ Let's Encrypt

```bash
sudo certbot --nginx -d your-domain.com -d www.your-domain.com
```

Làm theo hướng dẫn trên màn hình.

### 6.2 Kiểm tra SSL

Truy cập `https://your-domain.com` trong trình duyệt. Bạn sẽ thấy một biểu tượng khóa xanh.

### 6.3 Tự động gia hạn SSL

```bash
sudo systemctl enable certbot.timer
sudo systemctl start certbot.timer
```

## ✅ Bước 7: Kiểm Tra Chatbot

### 7.1 Health check

```bash
curl https://your-domain.com/health
```

Bạn sẽ thấy:
```json
{
  "status": "healthy",
  "service": "Facebook Messenger Chatbot",
  "timestamp": "2024-01-15T10:30:00"
}
```

### 7.2 Kiểm tra logs

```bash
sudo tail -f /var/log/chatbot.out.log
```

## 🔗 Bước 8: Kết Nối với Facebook

Trong Facebook Developers, thiết lập webhook URL:
```
https://your-domain.com/webhook
```

## 📊 Giám Sát & Bảo Trì

### Xem logs

```bash
# Logs từ chatbot
sudo tail -f /var/log/chatbot.out.log

# Logs từ Nginx
sudo tail -f /var/log/nginx/access.log
sudo tail -f /var/log/nginx/error.log
```

### Khởi động lại chatbot

```bash
sudo supervisorctl restart facebook-chatbot
```

### Kiểm tra tài nguyên

```bash
# CPU, RAM usage
top

# Disk usage
df -h

# Memory usage
free -h
```

## 🔄 Cập Nhật Code

Nếu bạn cần cập nhật code:

```bash
cd /home/facebook-chatbot
git pull origin main
pip3 install -r requirements.txt
sudo supervisorctl restart facebook-chatbot
```

## 🛡️ Bảo Mật

### Tạo firewall rules

```bash
# Cho phép SSH
sudo ufw allow 22/tcp

# Cho phép HTTP
sudo ufw allow 80/tcp

# Cho phép HTTPS
sudo ufw allow 443/tcp

# Bật firewall
sudo ufw enable
```

### Cập nhật hệ thống thường xuyên

```bash
apt-get update
apt-get upgrade -y
```

## ❓ Troubleshooting

### Lỗi: "Connection refused"

```bash
# Kiểm tra xem chatbot có chạy không
sudo supervisorctl status facebook-chatbot

# Nếu không chạy, khởi động lại
sudo supervisorctl restart facebook-chatbot
```

### Lỗi: "502 Bad Gateway"

```bash
# Kiểm tra logs Nginx
sudo tail -f /var/log/nginx/error.log

# Kiểm tra xem port 8000 có mở không
netstat -tlnp | grep 8000
```

### Lỗi: "SSL certificate error"

```bash
# Gia hạn SSL
sudo certbot renew

# Hoặc tạo mới
sudo certbot --nginx -d your-domain.com
```

## 📞 Hỗ Trợ

Nếu bạn gặp vấn đề:
1. Kiểm tra logs: `sudo tail -f /var/log/chatbot.out.log`
2. Kiểm tra Nginx: `sudo nginx -t`
3. Kiểm tra supervisor: `sudo supervisorctl status`

---

**Chúc mừng! Chatbot của bạn đã được triển khai lên VPS! 🎉**
