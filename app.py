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
ANSWER_CALLBACK = f"{TELEGRAM_API}/answerCallbackQuery"


# ===== helpers =====
def send_message(chat_id: int, text: str, reply_markup=None):
    payload = {"chat_id": chat_id, "text": text}
    if reply_markup:
        payload["reply_markup"] = reply_markup
    requests.post(SEND_MESSAGE, json=payload, timeout=15)


def answer_callback(callback_query_id: str):
    requests.post(ANSWER_CALLBACK, json={"callback_query_id": callback_query_id}, timeout=15)


def pay_text() -> str:
    return (
        "💳 Варианты оплаты:\n\n"
        f"🧾 Stripe (картой):\n{PAYMENT_STRIPE}\n\n"
        f"🅿️ PayPal:\n{PAYMENT_PAYPAL}\n\n"
        "После оплаты напиши: ✅ Я оплатил"
    )


# ===== routes =====
@app.get("/")
def home():
    return "Bot is running"


@app.post("/telegram")
def telegram_webhook():
    update = request.get_json(force=True) or {}

    # 1) INLINE-КНОПКИ (нажатия)
    callback = update.get("callback_query")
    if callback:
        callback_id = callback.get("id")
        chat_id = callback["message"]["chat"]["id"]
        data = callback.get("data", "")

        if data == "pay":
            send_message(chat_id, pay_text())

        if callback_id:
            answer_callback(callback_id)

        return {"ok": True}

    # 2) Обычные сообщения
    message = update.get("message")
    if not message:
        return {"ok": True}

    chat = message.get("chat")
    chat_id = chat.get("id") if chat else None
    if not chat_id:
        return {"ok": True}

    text = (message.get("text") or "").strip().lower()

    # /start
    if text.startswith("/start"):

    PHOTO_ID = "AgACAgIAAxkBAANgaX9rimvqHA6bLEuACyCwvhMetgwAAtMPax5A1Lu5DLF0zIez0BAAMCAAN5AAM4BA"

    requests.post(SEND_PHOTO, json={
        "chat_id": chat_id,
        "photo": PHOTO_ID,
        "caption": (
            "✨ Добро пожаловать в Алекса Quantum ✨\n\n"
            "Это бот медитаций.\n"
            "Здесь ты можешь познакомиться с проектом и перейти к оплате.\n\n"
            "Нажми кнопку ниже 👇"
        ),
        "reply_markup": {
            "inline_keyboard": [
                [{"text": "💳 Оплатить", "callback_data": "pay"}]
            ]
        }
    })

    return {"ok": True}


