import os
import requests
from flask import Flask, request

app = Flask(__name__)

# ===== ENV =====
BOT_TOKEN = os.environ.get("BOT_TOKEN")
PAYMENT_PAYPAL = os.environ.get("PAYMENT_PAYPAL", "")
PAYMENT_STRIPE = os.environ.get("PAYMENT_STRIPE", "")

if not BOT_TOKEN:
    raise RuntimeError("BOT_TOKEN is not set")

TELEGRAM_API = f"https://api.telegram.org/bot{BOT_TOKEN}"
SEND_MESSAGE = f"{TELEGRAM_API}/sendMessage"
SEND_PHOTO = f"{TELEGRAM_API}/sendPhoto"


# ===== ROOT =====
@app.get("/")
def home():
    return "Bot is running"


# ===== WEBHOOK =====
@app.post("/telegram")
def telegram_webhook():
    update = request.get_json(force=True)
    message = update.get("message")

    if not message:
        return {"ok": True}

    chat = message.get("chat")
    chat_id = chat.get("id") if chat else None
    text = (message.get("text") or "").lower()

    if not chat_id:
        return {"ok": True}

    # ===== /start =====
    if text.startswith("/start"):
        PHOTO_ID = AgACAgIAAxkBAAMvaX5p7ZmD7em8j6Jt20Gla-IHVRoAAisSaxs6AfFLQC5VHKe33fMBAAMCAAN5AAM4BA

        requests.post(
            SEND_PHOTO,
            json={
                "chat_id": chat_id,
                "photo": PHOTO_ID,
                "caption": (
                    "✨ Добро пожаловать в Lexxa Quantum ✨\n\n"
                    "Это бот медитаций.\n"
                    "Здесь ты можешь познакомиться с проектом и перейти к оплате.\n\n"
                    "Нажми кнопку ниже 👇"
                )
            }
        )
        return {"ok": True}

    # ===== /оплатить =====
    if text in ("/оплатить", "оплатить"):
        pay_text = (
            "💳 Варианты оплаты:\n\n"
            f"Stripe:\n{PAYMENT_STRIPE}\n\n"
            f"PayPal:\n{PAYMENT_PAYPAL}\n\n"
            "После оплаты напиши: Я оплатил"
        )
        requests.post(
            SEND_MESSAGE,
            json={
                "chat_id": chat_id,
                "text": pay_text
            }
        )
        return {"ok": True}

    return {"ok": True}


# ===== START SERVER =====
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)


