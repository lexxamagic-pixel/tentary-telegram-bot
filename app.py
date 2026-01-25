import os
import json
import stripe
import requests
from flask import Flask, request

app = Flask(__name__)

stripe.api_key = os.environ.get("STRIPE_SECRET_KEY")
BOT_TOKEN = os.environ.get("BOT_TOKEN")

TELEGRAM_API = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

@app.route("/")
def home():
    return "Bot is running"

@app.route("/stripe", methods=["POST"])
def stripe_webhook():
    payload = request.data
    event = stripe.Event.construct_from(
        json.loads(payload), stripe.api_key
    )

    if event["type"] == "checkout.session.completed":
        session = event["data"]["object"]
        email = session.get("customer_details", {}).get("email")
        print("PAID:", email)

    return "ok"
