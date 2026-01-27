import os
import requests
from flask import Flask, request

app = Flask(__name__)

BOT_TOKEN = os.environ.get("BOT_TOKEN")
TELEGRAM_API = f"https://api.telegram.org/bot{BOT_TOKEN}"

def send_message(chat_id, text):
    url = f"{TELEGRAM_API}/sendMessage"
    payload = {
        "chat_id": chat_id,
        "text": text
    }
    requests.post(url, json=payload)

@app.route("/")
def index():
    return "Bot is running"

@app.route("/telegram", methods=["POST"])
def telegram_webhook():
    update = request.get_json(silent=True) or {}

    message = update.get("message") or update.get("edited_message")
    if not message:
        return "ok"

    chat = message.get("chat", {})
    chat_id = chat.get("id")

    text = (message.get("text") or "").strip().lower()

    if chat_id and (text == "/start" or text == "start"):
        reply = (
            "Вас кап дизер вот?\n\n"
            "Доступ в закрытый канал с пакетом медитаций.\n"
            "Цена: 22 €\n\n"
            "Как это работает:\n"
            "1. Оплата\n"
            "2. Добавление в закрытый канал\n"
            "3. Первая медитация уже внутри\n"
        )
        send_message(chat_id, reply)

    return "ok"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
