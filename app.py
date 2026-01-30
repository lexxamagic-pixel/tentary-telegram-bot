import os
import requests
from flask import Flask, request

app = Flask(__name__)

# ====== ENV ======
BOT_TOKEN = os.environ.get("BOT_TOKEN")
PAYMENT_PAYPAL = os.environ.get("PAYMENT_PAYPAL", "")
PAYMENT_STRIPE = os.environ.get("PAYMENT_STRIPE", "")

if not BOT_TOKEN:
    raise RuntimeError("BOT_TOKEN is not set in Environment variables")

TELEGRAM_API = f"https://api.telegram.org/bot{BOT_TOKEN}"
TELEGRAM_SEND = f"{TELEGRAM_API}/sendMessage"

# ====== ROOT ======
@app.get("/")
def home():
    return "Bot is running"

# ====== HELPERS ======
def send_message(chat_id: int, text: str, reply_markup=None):
    payload = {"chat_id": chat_id, "text": text}
    if reply_markup:
        payload["reply_markup"] = reply_markup
    requests.post(TELEGRAM_SEND, json=payload, timeout=15)

# ====== TELEGRAM WEBHOOK ======
@app.post("/telegram")
def telegram_webhook():
    update = request.get_json(force=True, silent=True) or {}

    message = update.get("message") or update.get("edited_message")
    if not message:
        return "ok"

    chat = message.get("chat") or {}
    chat_id = chat.get("id")
    text = (message.get("text") or "").strip()

    if not chat_id or not text:
        return "ok"

    text_l = text.lower()

    # 1) Первая страница: приветствие + кнопка "Оплатить"
    if text_l.startswith("/start") or text_l in ("start", "старт"):
        welcome = (
            "Добро пожаловать 👋\n\n"
            "Это бот доступа в закрытый канал с медитациями.\n"
            "Цена: 22 €\n\n"
            "Нажмите кнопку ниже, чтобы перейти к оплате ⬇️"
        )
        keyboard = {
            "keyboard": [[{"text": "💳 Оплатить доступ"}]],
            "resize_keyboard": True,
            "one_time_keyboard": True
        }
        send_message(chat_id, welcome, reply_markup=keyboard)
        return "ok"

    # 2) Вторая страница: оплата
    if text_l == "💳 оплатить доступ".lower() or text_l == "оплатить доступ":
        pay_text = (
            "💳 Оплата доступа\n\n"
            "Цена: 22 €\n\n"
            f"💳 Stripe:\n{PAYMENT_STRIPE if PAYMENT_STRIPE else '— (не задано)'}\n\n"
            f"💙 PayPal:\n{PAYMENT_PAYPAL if PAYMENT_PAYPAL else '— (не задано)'}\n\n"
            "После оплаты напишите: Я оплатил"
        )
        keyboard = {
            "keyboard": [[{"text": "✅ Я оплатил"}]],
            "resize_keyboard": True
        }
        send_message(chat_id, pay_text, reply_markup=keyboard)
        return "ok"

    # 3) Подтверждение оплаты (пока просто ответ)
    if text_l in ("я оплатил", "оплатил", "✅ я оплатил"):
        reply = (
            "Спасибо! ✅\n\n"
            "Напишите, пожалуйста, имя/почту, которые указали в платеже, "
            "и я проверю оплату."
        )
        send_message(chat_id, reply)
        return "ok"

    # 4) Любое другое сообщение
    send_message(chat_id, 'Напишите /start, чтобы начать.')
    return "ok"


# ====== START SERVER ======
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)

