import os
import json

# 📁 Ensure data directory exists
os.makedirs("data", exist_ok=True)

# 📄 File paths
SPLASH_FILE = "data/splash247_articles.json"
MERGED_OUTPUT = "data/super_headlines.json"

# 🧪 Check if splash file exists
if not os.path.exists(SPLASH_FILE):
    print("⚠️ Splash247 data not found. Skipping merge.")
    exit(1)

# 🧠 Load Splash247 articles
try:
    with open(SPLASH_FILE, "r") as f:
        splash_articles = json.load(f)
except Exception as e:
    print("❌ Error reading splash file:", e)
    exit(1)

# 🧬 You could load other sources here and merge them later
merged_articles = splash_articles  # For now, just Splash247

# 💾 Save merged file
try:
    with open(MERGED_OUTPUT, "w") as f:
        json.dump(merged_articles, f, indent=2)
    print(f"✅ Merged {len(merged_articles)} articles to {MERGED_OUTPUT}")
except Exception as e:
    print("❌ Error saving merged file:", e)
    exit(1)
