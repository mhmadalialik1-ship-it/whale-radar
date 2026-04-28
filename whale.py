import logging
import httpx
import uvicorn
from fastapi import FastAPI, Request, BackgroundTasks

# --- Logging Setup ---
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()

# --- Configuration ---
# ملاحظة: تأكد من صحة التوكن والـ ID
BOT_TOKEN = "8763940647:AAH0wUlXobDpem8k610aIUvzvCo8K1bmvRc"

ADMIN_ID = 7974966998
TELEGRAM_URL = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

# Async HTTP Client for better performance
http_client = httpx.AsyncClient()

@app.on_event("shutdown")
async def shutdown_event():
    await http_client.aclose()

@app.get("/")
async def root():
    return {"status": "Whale Radar active", "network": "Solana"}

# --- Function to send the message ---
async def send_telegram_msg(activity: dict):
    try:
        description = activity.get("description", "No description")
        signature = activity.get("signature", "No Signature")
        signer = activity.get("feePayer", "N/A")

        # Formatting the message for Telegram
        msg_text = (
            f"🔹 *Whale Alert!*\n\n"
            f"👤 *Wallet:* `{signer}`\n"
            f"📝 *Activity:* {description}\n\n"
            f"🔗 [View on Solscan](https://solscan.io/tx/{signature})"
        )

        payload = {
            "chat_id": ADMIN_ID,
            "text": msg_text,
            "parse_mode": "Markdown",
            "disable_web_page_preview": False
        }

        response = await http_client.post(TELEGRAM_URL, json=payload)
        
        if response.status_code == 200:
            logger.info("Notification sent successfully to Telegram")
        else:
            logger.error(f"Telegram API Error: {response.status_code} - {response.text}")

    except Exception as e:
        logger.error(f"Error while processing message: {e}")

# --- Webhook Endpoint to receive data ---
@app.post("/webhook")
async def handle_webhook(request: Request, background_tasks: BackgroundTasks):
    try:
        data = await request.json()
        
        # التحقق مما إذا كانت البيانات قائمة أو معاملة واحدة
        if isinstance(data, list):
            for activity in data:
                background_tasks.add_task(send_telegram_msg, activity)
        else:
            background_tasks.add_task(send_telegram_msg, data)

        return {"status": "received"}
        
    except Exception as e:
        logger.error(f"Webhook error: {e}")
        return {"status": "error", "message": str(e)}

# --- Entry Point ---
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)


