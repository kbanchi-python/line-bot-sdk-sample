import os
from dotenv import load_dotenv
from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage, ImageSendMessage, StickerMessage

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
    if "いぬ" in sent_message:
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=f"{sent_message}わん"))
    elif "画像" in sent_message:
        image_url = "https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEhnhnvT4_2cxoFHgNG2slYCqxy6PTr5L_hrgN6lvm_fFNvtp_1UXELKAD1A3rRY9kgb6yCHKnTH7tTG9QJIrs0ZCnLDpoHaWRUiHWm03l9lbeooMzw9nZqt8PVDFJcUhxu8qu-I4H2HnN8/s800/kid_job_boy_programmer.png"
        line_bot_api.reply_message(
            event.reply_token,
            ImageSendMessage(
                original_content_url=image_url,
                preview_image_url=image_url
            ))
    elif "スタンプ" in sent_message:
        package_id = "8522"
        sticker_id = "16581266"
        line_bot_api.reply_message(
            event.reply_token,
            StickerMessage(package_id=package_id, sticker_id=sticker_id))
    else:
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=sent_message))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001)
