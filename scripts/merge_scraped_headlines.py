import os
import json
from datetime import datetime

SCRAPER_OUTPUTS = [
    "data/splash247_articles.json",
    # Future scrapers: add paths here
    # "data/reddit_posts.json",
    # "data/freightos_blog.json",
]

MERGED_OUTPUT = "data/super_headlines.json"

def merge_sources():
    merged = []
    for file in SCRAPER_OUTPUTS:
        if os.path.exists(file):
            with open(file, "r") as f:
                try:
                    merged.extend(json.load(f))
                except json.JSONDecodeError:
                    print(f"⚠️ Could not parse: {file}")
        else:
            print(f"❌ Missing file: {file}")

    # Add timestamp for traceability
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    merged_output = {
        "generated_at": timestamp,
        "sources": SCRAPER_OUTPUTS,
        "headlines": merged
    }

    with open(MERGED_OUTPUT, "w") as f:
        json.dump(merged_output, f, indent=2)
    print(f"✅ Merged {len(merged)} headlines into {MERGED_OUTPUT}")

if __name__ == "__main__":
    merge_sources()
