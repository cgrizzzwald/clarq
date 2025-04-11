import requests
from bs4 import BeautifulSoup
from datetime import datetime
import json
import os

def fetch_splash247_articles(limit=5):
    url = "https://splash247.com/category/news/"
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")

    articles = []
    posts = soup.find_all("article", class_="jeg_post")[:limit]

    for post in posts:
        try:
            title_tag = post.find("h3", class_="jeg_post_title")
            if not title_tag:
                continue
            link_tag = title_tag.find("a")
            snippet = post.find("div", class_="jeg_post_excerpt")

            title = link_tag.text.strip()
            url = link_tag["href"]
            summary = snippet.text.strip() if snippet else ""
            date = datetime.now().strftime("%Y-%m-%d")

            articles.append({
                "source": "Splash247",
                "title": title,
                "summary": summary,
                "link": url,
                "date": date,
                "category": "logistics"
            })
        except Exception as e:
            print("⚠️ Skipped article due to error:", e)

    return articles

# 🔥 This is the part that was missing
if __name__ == "__main__":
    articles = fetch_splash247_articles()

    if not articles:
        print("⚠️ No articles fetched. Skipping save.")
        exit(1)

    os.makedirs("data", exist_ok=True)

    with open("data/splash247_articles.json", "w") as f:
        json.dump(articles, f, indent=2)

    print(f"✅ Saved {len(articles)} Splash247 articles to data/splash247_articles.json")
