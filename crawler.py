import requests
from bs4 import BeautifulSoup
import json
import os

def crawl_yahoo_stock(query="財經"):
    url = "https://tw.stock.yahoo.com/rss"
    headers = {"User-Agent": "Mozilla/5.0"}
    try:
        res = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(res.text, "xml")
        news_list = []
        items = soup.find_all("item")[:5]

        for item in items:
            news_list.append({
                "title": item.title.text,
                "link": item.link.text
            })

        current_dir = os.path.dirname(os.path.abspath(__file__))
        data_dir = os.path.join(current_dir, "..", "data")
        
        if not os.path.exists(data_dir):
            os.makedirs(data_dir)

        file_path = os.path.join(data_dir, "news.json")
        
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(news_list, f, ensure_ascii=False, indent=2)
        
        return news_list
    except Exception as e:
        print(f"爬蟲出錯: {e}")
        return []
