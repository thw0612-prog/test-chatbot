from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage
from bot.linebot import build_smart_message

app = Flask(__name__)
import os

# 改成從系統環境變數讀取
LINE_CHANNEL_ACCESS_TOKEN = os.getenv('LINE_CHANNEL_ACCESS_TOKEN')
LINE_CHANNEL_SECRET = os.getenv('LINE_CHANNEL_SECRET')

#LINE_CHANNEL_ACCESS_TOKEN = "D+46QbNRN+XD7SPf5hbGu4e+lKPGe8yBNYvYtcHWmG9qjDXGrmdEkTmqhxt6+QcbzhQzjWr98OG6U+4W79DnVfqIKoNgbWUkD5BL1/HRfwmqmIG2YGzgFry+4Wyjr+23LeAaHHgdgFmTO5arumONDAdB04t89/1O/w1cDnyilFU="
#LINE_CHANNEL_SECRET = "d7c3129fbcb002294220eb30b6b1ffcd"

line_bot_api = LineBotApi(LINE_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(LINE_CHANNEL_SECRET)

@app.route("/callback", methods=["POST"])
def callback():
    signature = request.headers.get('X-Line-Signature')
    body = request.get_data(as_text=True)
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return "OK", 200

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    if event.message.text == "財經":
        # ⭐ 注意：這裡拿到的已經是完整的訊息物件了
        reply_obj = build_smart_message(event.message.text)
        
        line_bot_api.reply_message(
            event.reply_token,
            reply_obj # 👈 直接丟入物件
        )
if __name__ == "__main__":
    app.run(port=5000)