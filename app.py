import os
import json
from flask import Flask, request

import stripe

app = Flask(__name__)

@app.get("/")
def home():
    return "Bot is running"

@app.post("/stripe")
def stripe_webhook():
    # Проверяем, что ключ Stripe задан в Render Environment
    stripe_key = os.environ.get("STRIPE_SECRET_KEY")
    if not stripe_key:
        return ("Missing STRIPE_SECRET_KEY in environment", 500)

    stripe.api_key = stripe_key

    # Stripe может прислать JSON, читаем безопасно
    try:
        payload = request.get_data(as_text=True)  # str
        data = json.loads(payload) if payload else {}
    except Exception:
        return ("Invalid JSON", 400)

    event_type = data.get("type")

    if event_type == "checkout.session.completed":
        session = data.get("data", {}).get("object", {})
        email = (session.get("customer_details") or {}).get("email")
        # Пока просто логируем (будет видно в Render Logs)
        print("PAID:", email)

    return ("ok", 200)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", "10000"))
    app.run(host="0.0.0.0", port=port)
