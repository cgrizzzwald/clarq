
import requests
from bs4 import BeautifulSoup
from datetime import datetime
import json
import os

def fetch_supplychaindive_articles(limit=5):
    url = "https://www.supplychaindive.com/"
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")

    articles = []
    cards = soup.select(".article-feed .card")[:limit]

    for card in cards:
        try:
            title_tag = card.find("h3")
            link_tag = card.find("a", href=True)
            summary_tag = card.find("p")

            title = title_tag.text.strip() if title_tag else ""
            url = "https://www.supplychaindive.com" + link_tag["href"] if link_tag else ""
            summary = summary_tag.text.strip() if summary_tag else ""
            date = datetime.now().strftime("%Y-%m-%d")

            articles.append({
                "source": "SupplyChainDive",
                "title": title,
                "summary": summary,
                "link": url,
                "date": date,
                "category": "supply_chain",
                "severity": None
            })
        except Exception as e:
            print("⚠️ Skipped article due to error:", e)

    return articles

if __name__ == "__main__":
    articles = fetch_supplychaindive_articles()
    os.makedirs("data", exist_ok=True)
    with open("data/supplychaindive_articles.json", "w") as f:
        json.dump(articles, f, indent=2)
    print(f"✅ Saved {len(articles)} SupplyChainDive articles to data/supplychaindive_articles.json")
