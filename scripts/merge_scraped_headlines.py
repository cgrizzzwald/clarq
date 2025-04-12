import json
import os

merged = []

# List of source files to try to merge
sources = [
    "data/splash247_articles.json",
    # add more here later (e.g. data/supplychaindive_articles.json)
]

for path in sources:
    if os.path.exists(path):
        with open(path) as f:
            try:
                articles = json.load(f)
                if isinstance(articles, list):
                    merged.extend(articles)
                    print(f"✅ Merged {len(articles)} from {path}")
                else:
                    print(f"⚠️ Skipped {path}: not a list")
            except Exception as e:
                print(f"❌ Failed to read {path}: {e}")
    else:
        print(f"⚠️ File not found: {path}")

if merged:
    with open("data/merged_articles.json", "w") as f:
        json.dump(merged, f, indent=2)
    print(f"✅ Saved {len(merged)} merged articles to data/merged_articles.json")
else:
    print("⚠️ No articles to merge.")
