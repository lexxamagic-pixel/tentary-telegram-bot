import os
import requests
from flask import Flask, request

app = Flask(__name__)

BOT_TOKEN = os.environ.get("BOT_TOKEN")
PAYMENT_LINK = os.environ.get("PAYMENT_LINK", "https://example.com")

TELEGRAM_API = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"


@app.get("/")
def home():
    return "Bot is running"


@app.post("/telegram")
def telegram_webhook():
    update = request.get_json(silent=True) or {}

    message = update.get("message") or update.get("edited_message") or {}
    chat = message.get("chat") or {}
    chat_id = chat.get("id")

    text = (message.get("text") or "").strip().lower()

    if chat_id and text in ("/start", "start"):
        reply = (
            "Привет 👋\n\n"
            "Доступ в закрытый канал с медитациями.\n"
            "Цена: 22 €\n\n"
            f"Ссылка на оплату:\n{PAYMENT_LINK}\n\n"
            "После оплаты напишите:\nЯ оплатил"
        )

        requests.post(
            TELEGRAM_API,
            json={"chat_id": chat_id, "text": reply}
        )

    return {"ok": True}


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
