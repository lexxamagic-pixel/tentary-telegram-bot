import os
import requests
from flask import Flask, request

app = Flask(__name__)
print("### VERSION: 2026-02-03 A ###", flush=True)
TENTARY_URL = os.environ.get("TENTARY_URL", "").strip()

BOT_TOKEN = os.environ.get("BOT_TOKEN", "")
if not BOT_TOKEN:
    # Чтобы сразу было понятно в логах, почему не работает
    raise RuntimeError("BOT_TOKEN is not set in Environment Variables")

API = f"https://api.telegram.org/bot{BOT_TOKEN}"
SEND_MESSAGE = f"{API}/sendMessage"
SEND_PHOTO = f"{API}/sendPhoto"

    @app.get("/")
def index():
    return "Bot is running | VERSION 2026-02-03 A", 200



@app.post("/telegram")
def telegram_webhook():
    data = request.get_json(silent=True) or {}
    print("INCOMING UPDATE:", data)

    # 1) Обрабатываем обычные сообщения
    message = data.get("message")
    if message:
        chat = message.get("chat") or {}
        chat_id = chat.get("id")

        text = (message.get("text") or "").strip()
        text_lc = text.lower()

        if not chat_id:
            return {"ok": True}

        # /start (учитывает /start@botname)
        if text_lc.startswith("/start"):
            # Если не нужна картинка — закомментируй блок sendPhoto и включи sendMessage ниже.
            PHOTO_ID = "PASTE_YOUR_FILE_ID_HERE"

            caption = (
                "✨ Добро пожаловать в Алекса Quantum ✨\n\n"
                "Это бот медитаций.\n"
                "Нажми кнопку ниже 👇"
            )

           keyboard = {"inline_keyboard": []}

# 1) Медитации (одна кнопка)
if MEDITATIONS_URL:
    keyboard["inline_keyboard"].append(
        [{"text": "✉️ Получить медитации", "url": MEDITATIONS_URL}]
    )

            # Если PHOTO_ID не вставлен — отправим просто текст
            if PHOTO_ID and PHOTO_ID != "PASTE_YOUR_FILE_ID_HERE":
                r = requests.post(
                    SEND_PHOTO,
                    json={
                        "chat_id": chat_id,
                        "photo": PHOTO_ID,
                        "caption": caption,
                        "reply_markup": keyboard,
                    },
                    timeout=15,
                )
            else:
                r = requests.post(
                    SEND_MESSAGE,
                    json={
                        "chat_id": chat_id,
                        "text": caption,
                        "reply_markup": keyboard,
                    },
                    timeout=15,
                )

            # на всякий случай логируем ответ телеги в логи Render
            print("START send response:", r.status_code, r.text)
            return {"ok": True}

        # Любой другой текст
        requests.post(
            SEND_MESSAGE,
            json={
                "chat_id": chat_id,
                "text": "Напиши /start 🙂",
            },
            timeout=15,
        )
        return {"ok": True}

# 1) Медитации (одна кнопка)
if MEDITATIONS_URL:
    keyboard["inline_keyboard"].append(
        [{"text": "✉️ Получить медитации", "url": MEDITATIONS_URL}]
    )

# 2) Купить в Tentary
if TENTARY_URL:
    keyboard["inline_keyboard"].append(
        [{"text": "💳 Купить медитации", "url": TENTARY_URL}]
    )

if __name__ == "__main__":
    # Render сам даёт PORT
    port = int(os.environ.get("PORT", "10000"))
    app.run(host="0.0.0.0", port=port)




