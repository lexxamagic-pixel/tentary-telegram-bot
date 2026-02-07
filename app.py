import os
import requests
from flask import Flask, request

app = Flask(__name__)

BOT_TOKEN = os.environ.get("BOT_TOKEN", "")
TENTARY_URL = os.environ.get("TENTARY_URL", "").strip()

if not BOT_TOKEN:
    raise RuntimeError("BOT_TOKEN is not set")

@app.get("/")
def index():
    return "Bot is running | VERSION 2026-02-03 A", 200

@app.post("/telegram")
def telegram_webhook():
    return {"ok": True}




