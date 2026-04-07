"""
Facebook Messenger Chatbot with OpenAI Integration
Chatbot AI thông minh cho Facebook Fanpage
"""

from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import PlainTextResponse
import requests
import json
import os
from openai import OpenAI
import logging
from datetime import datetime

# Cấu hình logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Khởi tạo FastAPI
app = FastAPI()

# Lấy token từ environment variables
FACEBOOK_PAGE_ACCESS_TOKEN = os.getenv("FACEBOOK_PAGE_ACCESS_TOKEN", "YOUR_PAGE_ACCESS_TOKEN")
FACEBOOK_VERIFY_TOKEN = os.getenv("FACEBOOK_VERIFY_TOKEN", "your_verify_token")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Khởi tạo OpenAI client
try:
    client = OpenAI(api_key=OPENAI_API_KEY)
except Exception as e:
    logger.warning(f"OpenAI client initialization warning: {e}")
    client = None

# Lưu trữ conversation history cho mỗi user
conversation_history = {}

def get_conversation_history(sender_id):
    """Lấy lịch sử trò chuyện của user"""
    if sender_id not in conversation_history:
        conversation_history[sender_id] = []
    return conversation_history[sender_id]

def add_to_history(sender_id, role, content):
    """Thêm tin nhắn vào lịch sử trò chuyện"""
    history = get_conversation_history(sender_id)
    history.append({"role": role, "content": content})
    # Giữ lại 20 tin nhắn gần nhất để tránh quá dài
    if len(history) > 20:
        conversation_history[sender_id] = history[-20:]

def get_ai_response(sender_id, user_message):
    """Gọi OpenAI API để lấy phản hồi"""
    try:
        # Kiểm tra xem client có khởi tạo thành công không
        if not client:
            return "Xin lỗi, chatbot chưa được cấu hình đầy đủ. Vui lòng liên hệ quản lý."
        
        # Thêm tin nhắn của user vào lịch sử
        add_to_history(sender_id, "user", user_message)
        
        # Lấy lịch sử trò chuyện
        history = get_conversation_history(sender_id)
        
        # Gọi OpenAI API
        response = client.chat.completions.create(
            model="gpt-4.1-mini",
            messages=[
                {
                    "role": "system",
                    "content": """Bạn là một trợ lý chatbot thân thiện cho fanpage Facebook. 
                    Hãy trả lời các câu hỏi một cách ngắn gọn, hữu ích và thân thiện.
                    Nếu bạn không biết câu trả lời, hãy nói rằng bạn sẽ liên hệ với quản lý fanpage.
                    Luôn sử dụng tiếng Việt để trả lời."""
                }
            ] + history,
            max_tokens=500,
            temperature=0.7
        )
        
        ai_message = response.choices[0].message.content
        
        # Thêm phản hồi AI vào lịch sử
        add_to_history(sender_id, "assistant", ai_message)
        
        return ai_message
    
    except Exception as e:
        logger.error(f"Lỗi khi gọi OpenAI API: {str(e)}")
        return "Xin lỗi, tôi gặp lỗi kỹ thuật. Vui lòng thử lại sau."

def send_message_to_facebook(recipient_id, message_text):
    """Gửi tin nhắn đến Facebook Messenger"""
    try:
        url = f"https://graph.facebook.com/v18.0/me/messages"
        
        payload = {
            "recipient": {"id": recipient_id},
            "message": {"text": message_text}
        }
        
        params = {"access_token": FACEBOOK_PAGE_ACCESS_TOKEN}
        
        response = requests.post(url, json=payload, params=params)
        
        if response.status_code != 200:
            logger.error(f"Lỗi gửi tin nhắn: {response.text}")
            return False
        
        logger.info(f"Tin nhắn đã gửi cho {recipient_id}")
        return True
    
    except Exception as e:
        logger.error(f"Lỗi khi gửi tin nhắn: {str(e)}")
        return False

@app.get("/webhook")
async def verify_webhook(request: Request):
    """Xác minh webhook với Facebook"""
    try:
        verify_token = request.query_params.get("hub.verify_token")
        challenge = request.query_params.get("hub.challenge")
        
        if verify_token == FACEBOOK_VERIFY_TOKEN:
            logger.info("Webhook xác minh thành công")
            return PlainTextResponse(challenge)
        else:
            logger.error("Verify token không hợp lệ")
            raise HTTPException(status_code=403, detail="Invalid verify token")
    
    except Exception as e:
        logger.error(f"Lỗi xác minh webhook: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/webhook")
async def handle_webhook(request: Request):
    """Xử lý tin nhắn từ Facebook"""
    try:
        body = await request.json()
        
        # Kiểm tra xem đây có phải là message event không
        if body.get("object") != "page":
            return {"status": "ok"}
        
        # Xử lý từng entry
        for entry in body.get("entry", []):
            for messaging_event in entry.get("messaging", []):
                sender_id = messaging_event.get("sender", {}).get("id")
                recipient_id = messaging_event.get("recipient", {}).get("id")
                
                # Xử lý tin nhắn text
                if messaging_event.get("message"):
                    message = messaging_event["message"]
                    
                    # Bỏ qua tin nhắn echo (do chatbot gửi)
                    if message.get("is_echo"):
                        continue
                    
                    user_message = message.get("text", "")
                    
                    if user_message:
                        logger.info(f"Tin nhắn từ {sender_id}: {user_message}")
                        
                        # Gọi AI để lấy phản hồi
                        ai_response = get_ai_response(sender_id, user_message)
                        
                        # Gửi phản hồi về Facebook
                        send_message_to_facebook(sender_id, ai_response)
                
                # Xử lý postback (khi user click button)
                elif messaging_event.get("postback"):
                    postback = messaging_event["postback"]
                    payload = postback.get("payload", "")
                    logger.info(f"Postback từ {sender_id}: {payload}")
        
        return {"status": "ok"}
    
    except Exception as e:
        logger.error(f"Lỗi xử lý webhook: {str(e)}")
        return {"status": "error", "message": str(e)}

@app.get("/")
async def root():
    """Health check endpoint"""
    return {
        "status": "running",
        "service": "Facebook Messenger Chatbot",
        "timestamp": datetime.now().isoformat()
    }

@app.get("/health")
async def health_check():
    """Kiểm tra sức khỏe dịch vụ"""
    return {
        "status": "healthy",
        "service": "Facebook Messenger Chatbot",
        "timestamp": datetime.now().isoformat()
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
