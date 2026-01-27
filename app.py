import os
import json
import requests
from flask import Flask, request

import stripe

app = Flask(__name__)

BOT_TOKEN = os.environ.get("BOT_TOKEN")
STRIPE_SECRET_KEY = os.environ.get("STRIPE_SECRET_KEY")

# сюда можешь поставить ссылку на оплату (Stripe Payment Link или Tentary)
PAYMENT_LINK = os.environ.get("PAYMENT_LINK", "https://paypal.me/alexandraprudius/22")

def tg_send(chat_id: int, text: str):
    if not BOT_TOKEN:
        return
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    requests.post(url, json={"chat_id": chat_id, "text": text})

@app.get("/")
def home():
    return "Bot is running"

# --- TELEGRAM WEBHOOK ---
@app.post("/telegram")
def telegram_webhook():
    update = request.get_json(silent=True) or {}
    message = update.get("message") or update.get("edited_message") or {}
    chat = message.get("chat") or {}
    chat_id = chat.get("id")

    t = (message.get("text") or "").strip()

if t.lower().startswith("/start") or t.lower() == "start":
    # ответ


    if chat_id and (text == "/start" or text.lower() == "start"):
        reply = (
            "Доступ в закрытый канал с пакетом медитаций.\n\n"
            "Цена: 22€\n\n"
            "Как это работает:\n"
            "1) Оплата\n"
            "2) Вы пишете сюда: Я оплатил(а)\n"
            "3) Мы добавляем вас в закрытый канал\n\n"
            f"Оплата: {PAYMENT_LINK}"
        )
        tg_send(chat_id, reply)

    return ("ok", 200)

# --- STRIPE WEBHOOK ---
@app.post("/stripe")
def stripe_webhook():
    if not STRIPE_SECRET_KEY:
        return ("Missing STRIPE_SECRET_KEY in environment", 500)

    stripe.api_key = STRIPE_SECRET_KEY

    payload = request.get_data(as_text=True)
    try:
        data = json.loads(payload) if payload else {}
    except Exception:
        return ("Invalid JSON", 400)

    event_type = data.get("type")
    if event_type == "checkout.session.completed":
        session = data.get("data", {}).get("object", {})
        email = (session.get("customer_details") or {}).get("email")
        print("PAID:", email)

    return ("ok", 200)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", "10000"))
    app.run(host="0.0.0.0", port=port)
