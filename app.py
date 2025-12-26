import os
from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage
from bot.linebot import build_smart_message

app = Flask(__name__)

# --- 安全性修改：從環境變數讀取金鑰 ---
# 在 Render 部署時，請在環境變數設定這兩個對應的 Key
LINE_CHANNEL_ACCESS_TOKEN = os.getenv('LINE_CHANNEL_ACCESS_TOKEN')
LINE_CHANNEL_SECRET = os.getenv('LINE_CHANNEL_SECRET')

line_bot_api = LineBotApi(LINE_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(LINE_CHANNEL_SECRET)

@app.route("/callback", methods=["POST"])
def callback():
    # 取得 LINE 傳來的簽章，確認來源安全
    signature = request.headers.get('X-Line-Signature')
    body = request.get_data(as_text=True)
    
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        # 如果簽章不符，代表請求可能被竄改，回報 400 錯誤
        abort(400)
    return "OK", 200

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    user_text = event.message.text.strip()
    
    if user_text == "財經":
        # 呼叫 bot/linebot.py 裡的邏輯，這會觸發爬蟲並生成 Flex Message
        reply_obj = build_smart_message(user_text)
        
        line_bot_api.reply_message(
            event.reply_token,
            reply_obj
        )
    else:
        # 如果不是輸入「財經」，可以選擇不回應或回傳簡單說明
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text="請輸入「財經」來獲取最新財經新聞要聞！")
        )

if __name__ == "__main__":
    # 在本機測試時使用 5000 端口，Render 部署時會自動分配
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)