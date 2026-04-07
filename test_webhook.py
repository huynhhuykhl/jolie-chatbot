"""
Script để test webhook chatbot
"""

import requests
import json
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Cấu hình
WEBHOOK_URL = "http://localhost:8000/webhook"
VERIFY_TOKEN = os.getenv("FACEBOOK_VERIFY_TOKEN", "your_verify_token")

def test_verify_webhook():
    """Test xác minh webhook"""
    print("🧪 Test xác minh webhook...")
    
    params = {
        "hub.mode": "subscribe",
        "hub.verify_token": VERIFY_TOKEN,
        "hub.challenge": "test_challenge_string"
    }
    
    response = requests.get(WEBHOOK_URL, params=params)
    
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.text}")
    
    if response.status_code == 200 and response.text == "test_challenge_string":
        print("✅ Webhook xác minh thành công!")
        return True
    else:
        print("❌ Webhook xác minh thất bại!")
        return False

def test_message_webhook():
    """Test gửi tin nhắn"""
    print("\n🧪 Test gửi tin nhắn...")
    
    payload = {
        "object": "page",
        "entry": [
            {
                "id": "page_id",
                "time": 1234567890,
                "messaging": [
                    {
                        "sender": {"id": "user_123"},
                        "recipient": {"id": "page_456"},
                        "timestamp": 1234567890,
                        "message": {
                            "mid": "mid_123",
                            "text": "Xin chào, bạn là ai?"
                        }
                    }
                ]
            }
        ]
    }
    
    response = requests.post(
        WEBHOOK_URL,
        json=payload,
        headers={"Content-Type": "application/json"}
    )
    
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.json()}")
    
    if response.status_code == 200:
        print("✅ Tin nhắn được xử lý thành công!")
        return True
    else:
        print("❌ Xử lý tin nhắn thất bại!")
        return False

def test_health_check():
    """Test health check"""
    print("\n🧪 Test health check...")
    
    response = requests.get("http://localhost:8000/health")
    
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.json()}")
    
    if response.status_code == 200:
        print("✅ Health check thành công!")
        return True
    else:
        print("❌ Health check thất bại!")
        return False

def main():
    """Chạy tất cả tests"""
    print("=" * 50)
    print("Facebook Chatbot Webhook Test")
    print("=" * 50)
    
    try:
        # Test health check trước
        test_health_check()
        
        # Test verify webhook
        test_verify_webhook()
        
        # Test message webhook
        test_message_webhook()
        
        print("\n" + "=" * 50)
        print("✅ Tất cả tests hoàn thành!")
        print("=" * 50)
    
    except requests.exceptions.ConnectionError:
        print("❌ Lỗi: Không thể kết nối đến webhook!")
        print("Hãy chắc chắn rằng chatbot đang chạy (python main.py)")
    except Exception as e:
        print(f"❌ Lỗi: {str(e)}")

if __name__ == "__main__":
    main()
