import os
import requests
from flask import Flask, request

app = Flask(__name__)

# ===== НАСТРОЙКИ =====
TOKEN = "ВСТАВЬ_СЮДА_ТОКЕН_БОТА"
API_URL = f"https://api.telegram.org/bot{TOKEN}"

SEND_MESSAGE = f"{API_URL}/sendMessage"
SEND_PHOTO = f"{API_URL}/sendPhoto"


@app.route("/", methods=["GET"])
def index():
    return "Bot is running"


@app.route("/telegram", methods=["POST"])
def telegram_webhook():
    data = request.get_json()

    if not data:
        return {"ok": True}

    message = data.get("message")
    if not message:
        return {"ok": True}

    chat = message.get("chat")
    chat_id = chat.get("id") if chat else None
    if not chat_id:
        return {"ok": True}

    text = (message.get("text") or "").strip().lower()

    # ===== /start =====
    if text.startswith("/start") or text in ("start", "старт"):
        PHOTO_ID = "AgACAgIAAxkBAANgaX9rimvqHA6bLEuACyCWvhMetgwAAtMPaxs6AflLu5DLF0zIezoBAAMCAAN5AAM4BA"

        requests.post(SEND_PHOTO, json={
            "chat_id": chat_id,
            "photo": PHOTO_ID,
            "caption": (
                "✨ Добро пожаловать в Alexa Quantum ✨\n\n"
                "Это бот медитаций.\n"
                "Здесь ты можешь познакомиться с проектом.\n\n"
                "Нажми кнопку ниже 👇"
            ),
            "reply_markup": {
                "inline_keyboard": [
                    [{"text": "💳 Оплатить", "callback_data": "pay"}]
                ]
            }
        })

        return {"ok": True}

    return {"ok": True}


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)



