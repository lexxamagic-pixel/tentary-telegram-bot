import os
import requests
from flask import Flask, request

app = Flask(__name__)

# ====== ENV ======
BOT_TOKEN = os.environ.get("BOT_TOKEN")
PAYMENT_PAYPAL = os.environ.get("PAYMENT_PAYPAL", "")
PAYMENT_STRIPE = os.environ.get("PAYMENT_STRIPE", "")

TELEGRAM_SEND = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"


# ====== ROOT ======
@app.get("/")
def home():
    return "Bot is running"


# ====== TELEGRAM WEBHOOK ======
@app.post("/telegram")
def telegram_webhook():
    update = request.get_json(force=True)

    message = update.get("message")
    if not message:
        return {"ok": True}

    chat = message.get("chat")
    text = message.get("text")

    if not chat or not text:
        return {"ok": True}

    chat_id = chat.get("id")
    text = text.strip().lower()

    if text.startswith("/start"):
        reply = (
            "Добро пожаловать 👋\n\n"
            "Доступ в закрытый закрытый канал с медитациями.\n"
            "Цена: 22 €\n\n"
            "Оплатить можно здесь:\n\n"
            f"💳 Stripe:\n{PAYMENT_STRIPE}\n\n"
            f"🅿️ PayPal:\n{PAYMENT_PAYPAL}\n\n"
            "После оплаты напишите: Я оплатил"
        )

        requests.post(
            TELEGRAM_SEND,
            json={
                "chat_id": chat_id,
                "text": reply
            }
        )

    return {"ok": True}


# ====== START SERVER ======
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
