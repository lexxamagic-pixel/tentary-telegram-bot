import os
import requests
from flask import Flask, request

app = Flask(__name__)

# ====== ENV ======
BOT_TOKEN = os.environ.get("BOT_TOKEN")
PAYMENT_PAYPAL = os.environ.get("PAYMENT_PAYPAL", "")
PAYMENT_STRIPE = os.environ.get("PAYMENT_STRIPE", "")

if not BOT_TOKEN:
    raise RuntimeError("BOT_TOKEN is not set")

TELEGRAM_API = f"https://api.telegram.org/bot{BOT_TOKEN}"
TELEGRAM_SEND = f"{TELEGRAM_API}/sendMessage"


# ====== HELPERS ======
def send_message(chat_id: int, text: str, reply_markup=None):
    payload = {"chat_id": chat_id, "text": text}
    if reply_markup:
        payload["reply_markup"] = reply_markup
    requests.post(TELEGRAM_SEND, json=payload, timeout=15)


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

    chat = message.get("chat") or {}
    chat_id = chat.get("id")
    if not chat_id:
        return {"ok": True}

    # 1) Если прислали фото — вернём file_id
    photos = message.get("photo")
    if photos:
        file_id = photos[-1]["file_id"]  # самое большое фото
        send_message(chat_id, f"📸 Фото получено!\n\nfile_id:\n{file_id}")
        return {"ok": True}

    # 2) Текст
    text = (message.get("text") or "").strip()
    if not text:
        return {"ok": True}

    text_l = text.lower()

    # Первая страница: /start
    if text_l.startswith("/start") or text_l in ("start", "старт"):
        welcome = (
            "✨ Добро пожаловать в Алекса Quantum ✨\n\n"
            "Это бот медитаций.\n"
            "Здесь ты можешь познакомиться с проектом и перейти к оплате.\n\n"
            "Нажми кнопку ниже:"
        )

        keyboard = {
            "inline_keyboard": [
                [{"text": "💳 Оплатить", "callback_data": "pay"}]
            ]
        }

        send_message(chat_id, welcome, reply_markup=keyboard)
        return {"ok": True}

    # Если человек пишет /оплатить
    if text_l in ("/оплатить", "/pay", "оплатить", "pay"):
        send_pay(chat_id)
        return {"ok": True}

    # Если написал "я оплатил" — пока просто ответ
    if "я оплатил" in text_l:
        send_message(
            chat_id,
            "✅ Спасибо! Напиши, пожалуйста, в поддержку или пришли скрин оплаты сюда — и мы дадим доступ."
        )
        return {"ok": True}

    # Любой другой текст
    send_message(
        chat_id,
        "Я понимаю команды:\n"
        "/start — начало\n"
        "/оплатить — варианты оплаты\n\n"
        "Можно отправить фото — я верну file_id."
    )
    return {"ok": True}


# ====== CALLBACKS (кнопки) ======
@app.post("/telegram_callback")
def telegram_callback():
    update = request.get_json(force=True)
    callback = update.get("callback_query")
    if not callback:
        return {"ok": True}

    chat_id = (callback.get("message") or {}).get("chat", {}).get("id")
    data = callback.get("data")

    # Обязательно отвечаем на callback, чтобы Telegram убрал "часики"
    callback_id = callback.get("id")
    if callback_id:
        requests.post(
            f"{TELEGRAM_API}/answerCallbackQuery",
            json={"callback_query_id": callback_id},
            timeout=15
        )

    if chat_id and data == "pay":
        send_pay(chat_id)

    return {"ok": True}


def send_pay(chat_id: int):
    stripe_line = f"💳 Оплата картой (Stripe):\n{PAYMENT_STRIPE}\n\n" if PAYMENT_STRIPE else ""
    paypal_line = f"🅿️ PayPal:\n{PAYMENT_PAYPAL}\n\n" if PAYMENT_PAYPAL else ""

    pay_text = (
        "💰 Варианты оплаты:\n\n"
        f"{stripe_line}"
        f"{paypal_line}"
        "После оплаты напиши: ✅ Я оплатил"
    )

    send_message(chat_id, pay_text)


# ====== START SERVER ======
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)

