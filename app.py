import os
import requests
from flask import Flask, request

app = Flask(__name__)

# ===== ENV =====
BOT_TOKEN = os.environ.get("BOT_TOKEN")
PAYMENT_PAYPAL = os.environ.get("PAYMENT_PAYPAL", "")
PAYMENT_STRIPE = os.environ.get("PAYMENT_STRIPE", "")

TELEGRAM_API = f"https://api.telegram.org/bot{BOT_TOKEN}"
SEND_MESSAGE = f"{TELEGRAM_API}/sendMessage"


# ===== ROOT =====
@app.get("/")
def home():
    return "Bot is running"


# ===== HELPER =====
def send_message(chat_id, text):
    requests.post(
        SEND_MESSAGE,
        json={
            "chat_id": chat_id,
            "text": text
        },
        timeout=15
    )


# ===== WEBHOOK =====
@app.post("/telegram")
def telegram_webhook():
    update = request.get_json(force=True)
    message = update.get("message")

    if not message:
        return {"ok": True}

    chat = message.get("chat")
    text = (message.get("text") or "").strip().lower()

    if not chat or not text:
        return {"ok": True}

    chat_id = chat.get("id")

    # ===== /start =====
    if text.startswith("/start"):
        welcome_text = (
            "✨ Добро пожаловать в Lexxa Quantum ✨\n\n"
            "Это бот медитаций.\n"
            "Здесь ты можешь познакомиться с проектом и перейти к оплате.\n\n"
            "Чтобы посмотреть варианты оплаты, напиши:\n"
            "👉 /оплатить"
        )
        send_message(chat_id, welcome_text)
        return {"ok": True}

    # ===== /оплатить =====
    if text.startswith("/оплатить") or text.startswith("/pay"):
        pay_text = (
            "💫 Доступ к медитациям Lexxa Quantum\n"
            "Цена: 22 €\n\n"
            "💳 Оплата картой (Stripe):\n"
            f"{PAYMENT_STRIPE}\n\n"
            "💙 Оплата через PayPal:\n"
            f"{PAYMENT_PAYPAL}\n\n"
            "После оплаты напиши: Я оплатил"
        )
        send_message(chat_id, pay_text)
        return {"ok": True}

    return {"ok": True}


# ===== START SERVER =====
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)

