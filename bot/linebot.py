import os
import sys
import importlib.util
from linebot.models import FlexSendMessage, TextSendMessage # 👈 增加匯入

# (原本的路徑載入 crawler 部分維持不變...)
current_dir = os.path.dirname(os.path.abspath(__file__))
crawler_path = os.path.join(current_dir, "..", "crawler", "crawler.py")
spec = importlib.util.spec_from_file_location("crawler", crawler_path)
crawler_module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(crawler_module)

def build_smart_message(user_input):
    try:
        news_data = crawler_module.crawl_yahoo_stock()
        if not news_data:
            return TextSendMessage(text="暫時無法取得新聞。")

        bubbles = []
        for n in news_data[:5]:
            # 建立單張卡片 (Bubble)
            bubble = {
                "type": "bubble",
                "size": "micro", # 縮小尺寸，適合滑動
                "body": {
                    "type": "box",
                    "layout": "vertical",
                    "contents": [
                        {
                            "type": "text",
                            "text": n['title'],
                            "weight": "bold",
                            "size": "sm",
                            "wrap": True,
                            "maxLines": 3,
                            "margin": "md"
                        }
                    ],
                    "paddingAll": "20px"
                },
                "footer": {
                    "type": "box",
                    "layout": "vertical",
                    "contents": [
                        {
                            "type": "button",
                            "style": "primary", # 實心按鈕
                            "color": "#1DB446",
                            "height": "sm",
                            "action": {
                                "type": "uri",
                                "label": "閱讀全文",
                                "uri": n['link']
                            }
                        }
                    ]
                }
            }
            bubbles.append(bubble)

        # 回傳 Flex Message 物件
        return FlexSendMessage(
            alt_text="📢 今日財經要聞",
            contents={
                "type": "carousel",
                "contents": bubbles
            }
        )
    except Exception as e:
        return TextSendMessage(text=f"發生錯誤：{e}")