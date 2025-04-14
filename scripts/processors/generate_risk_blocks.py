import json
import os
from collections import defaultdict

def load_articles(path):
    if not os.path.exists(path):
        print("⚠️ No merged_articles.json found.")
        return []
    with open(path) as f:
        return json.load(f)

def build_risk_blocks(articles):
    categories = defaultdict(list)
    for a in articles:
        cat = a.get("category", "general")
        categories[cat].append(a)

    blocks = []
    for cat, group in categories.items():
        descriptions = [a["summary"] for a in group if a.get("summary")]
        headlines = [{
            "title": a.get("title", "No Title"),
            "severity": a.get("severity", 3)
        } for a in group]

        avg_severity = round(sum(a.get("severity", 3) for a in group) / len(group), 1)

        blocks.append({
            "type": "risk",
            "category": cat.capitalize(),
            "description": descriptions[0] if descriptions else f"Recent updates tagged under {cat}.",
            "rating": int(avg_severity),
            "why_it_matters": "Based on recent headlines, this category has shown notable developments.",
            "impact": "May affect operations depending on severity and timing.",
            "suggested_action": "Review this category for potential risk exposure.",
            "headlines": headlines[:6],
            "trend": [avg_severity] * 30  # placeholder for now
        })

    return blocks

def build_summary(articles):
    if not articles:
        return {
            "type": "summary",
            "content": "No risk data available yet."
        }

    high_risk = sorted(articles, key=lambda x: x.get("severity", 3), reverse=True)[:1]
    return {
        "type": "summary",
        "content": f"{high_risk[0]['title']} — {high_risk[0]['summary']}" if high_risk else "Latest risks evaluated from current data."
    }

def build_rumor_block():
    # This can be updated with real inputs later
    return {
        "type": "rumor",
        "rumors": []
    }

def main():
    os.makedirs("data", exist_ok=True)
    articles = load_articles("data/merged_articles.json")

    risk_blocks = [build_summary(articles)]
    risk_blocks += build_risk_blocks(articles)
    risk_blocks.append(build_rumor_block())

    with open("risk_blocks_transformed.json", "w") as f:
        json.dump(risk_blocks, f, indent=2)
    print("✅ Updated risk_blocks_transformed.json")

if __name__ == "__main__":
    main()
