import requests
from bs4 import BeautifulSoup

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
        return news_list
    except Exception as e:
        print(f"爬蟲出錯: {e}")
        return []