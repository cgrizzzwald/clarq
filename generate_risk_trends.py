import json
from collections import defaultdict

# Load risk blocks
with open("risk_blocks_transformed.json", "r") as f:
    blocks = json.load(f)

# Initialize category-based trend map
trend_data = defaultdict(list)

# Build trend data by category
for block in blocks:
    if block.get("type") == "risk":
        category = block.get("category", "Uncategorized")
        if "trend" in block:
            trend_data[category].extend(block["trend"])
        elif "rating" in block:
            trend_data[category].append(block["rating"])

# Optional: Keep only the last 30 entries for each category
for category in trend_data:
    trend_data[category] = trend_data[category][-30:]

# Save the result to risk_trends.json
with open("risk_trends.json", "w") as f:
    json.dump(trend_data, f, indent=2)

print("✅ risk_trends.json updated.")
