from flask import Flask, request
import requests
import os

app = Flask(__name__)

TOKEN = "8742729664:AAHKmoy1S2mSOuYM06DQJMW651EAi32FFHs"
URL = f"https://api.telegram.org/bot{TOKEN}"


def send_message(chat_id, text):
    requests.post(
        f"{URL}/sendMessage",
        json={
            "chat_id": chat_id,
            "text": text
        },
        timeout=10
    )


@app.route("/", methods=["GET"])
def home():
    return "Bot is running", 200


@app.route("/", methods=["POST"])
def webhook():
    data = request.get_json(silent=True)

    if not data:
        return "no data", 200

    if "message" in data:
        message = data["message"]
        chat_id = message["chat"]["id"]
        text = message.get("text", "")

        if text == "/start":
            send_message(chat_id, "Ты уже здесь.\n\nПоезд движется.")
        else:
            send_message(chat_id, f"Ты написала: {text}")

    return "ok", 200


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
