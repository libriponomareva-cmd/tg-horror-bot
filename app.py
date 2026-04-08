from flask import Flask, request
import requests

app = Flask(__name__)

TOKEN = "ТВОЙ_ТОКЕН_БОТА"
URL = f"https://api.telegram.org/bot{TOKEN}"

def send_message(chat_id, text):
    requests.post(f"{URL}/sendMessage", json={
        "chat_id": chat_id,
        "text": text
    })

@app.route("/", methods=["POST"])
def webhook():
    data = request.get_json()

    if "message" in data:
        chat_id = data["message"]["chat"]["id"]
        text = data["message"].get("text", "")

        if text == "/start":
            send_message(chat_id, "Ты уже здесь.\n\nПоезд движется.")
        else:
            send_message(chat_id, "Я тебя услышал.")

    return "ok"

@app.route("/", methods=["GET"])
def home():
    import os

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
    return "Bot is running"
