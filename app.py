import os
from dotenv import load_dotenv
from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage

load_dotenv(verbose=True)

app = Flask(__name__)

line_bot_api = LineBotApi(os.environ['ACCESS_TOKEN'])
handler = WebhookHandler(os.environ['CHANNEL_SECRET'])

@app.route("/callback", methods=["POST"])
def callback():
    signature = request.headers["X-Line-Signature"]
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)
    try:
        handler.handle(body, signature)
    except InvalidSignatureError as e:
        abort(400)
    return "Callback OK"

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    sent_message = event.message.text
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=sent_message))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001)
