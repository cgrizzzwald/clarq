
import json
import os
from datetime import datetime

# Very basic keyword → category + severity score mapping
CATEGORY_MAP = {
    "tariff": ("customs", 7),
    "strike": ("labor", 8),
    "port": ("logistics", 6),
    "shipping": ("logistics", 5),
    "delay": ("logistics", 6),
    "shortage": ("supply", 7),
    "china": ("macro", 5),
    "india": ("macro", 5),
    "iphone": ("tech", 6),
    "ai": ("tech", 4),
    "customs": ("customs", 6),
    "shutdown": ("macro", 8),
}

def tag_and_score_article(article):
    score = 3
    category = "general"
    text = f"{article.get('title', '')} {article.get('summary', '')}".lower()

    for keyword, (cat, sev) in CATEGORY_MAP.items():
        if keyword in text:
            category = cat
            score = max(score, sev)

    article["category"] = category
    article["severity"] = score
    return article

def process_articles(input_path):
    with open(input_path) as f:
        articles = json.load(f)

    processed = [tag_and_score_article(a) for a in articles]

    with open(input_path, "w") as f:
        json.dump(processed, f, indent=2)

    print(f"✅ Tagged and scored {len(processed)} articles in {input_path}")

if __name__ == "__main__":
    os.makedirs("data", exist_ok=True)
    for filename in os.listdir("data"):
        if filename.endswith("_articles.json"):
            process_articles(os.path.join("data", filename))
