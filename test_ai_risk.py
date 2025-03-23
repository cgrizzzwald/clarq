from flask import Flask, jsonify, request, render_template
import os
import openai
import json
import urllib3
import certifi
import requests
from bs4 import BeautifulSoup
from googlesearch import search
from datetime import datetime, timezone

# === Setup ===
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
os.environ["SSL_CERT_FILE"] = certifi.where()
os.environ["REQUESTS_CA_BUNDLE"] = certifi.where()

app = Flask(__name__)
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise ValueError("❌ OPENAI_API_KEY environment variable not set.")
client = openai.OpenAI(api_key=api_key)

# === User Preferences ===
user_prefs = {
    "industries": ["Mobile Accessories", "Phone Cases"],
    "countries": ["China", "Vietnam", "Indonesia"],
    "shipping_modes": ["Ocean", "Air"]
}

# === Data Sources ===
freight_sources = {
    "Xeneta": "https://www.xeneta.com/",
    "SeaRates": "https://www.searates.com/",
    "Drewry WCI": "https://www.drewry.co.uk/supply-chain-advisors/supply-chain-expertise/world-container-index",
    "SCFI": "https://en.sse.net.cn/indices/scfinew.jsp",
    "IATA": "https://www.iata.org/en/publications/economics/"
}

news_sources = {
    "Google News": None,
    "TechCrunch - Mobile": "https://techcrunch.com/tag/mobile/",
    "Supply Chain Dive": "https://www.supplychaindive.com/",
    "Business of Fashion": "https://www.businessoffashion.com/",
    "SCMP - Supply Chain": "https://www.scmp.com/topics/supply-chains"
}

# === Data Collection ===
def get_freight_rates():
    rates = []
    for source, url in freight_sources.items():
        try:
            response = requests.get(url, headers={"User-Agent": "Mozilla/5.0"}, timeout=10)
            response.raise_for_status()
            rates.append({"source": source, "status": "Success", "url": url})
        except requests.RequestException as e:
            rates.append({"source": source, "status": f"Error: {e}", "url": url})
    return rates

def get_news_headlines():
    headlines = []
    try:
        query = "Mobile Accessories Supply Chain Risks 2024"
        results = search(query, num_results=5)
        headlines.append({"source": "Google News", "headlines": [{"headline": r, "url": r} for r in results]})
    except Exception as e:
        headlines.append({"source": "Google News", "error": f"Google News fetch failed: {e}"})
    
    for source, url in news_sources.items():
        if source == "Google News":
            continue
        try:
            res = requests.get(url, headers={"User-Agent": "Mozilla/5.0"}, timeout=10)
            res.raise_for_status()
            soup = BeautifulSoup(res.text, "html.parser")
            found = [h.get_text(strip=True) for h in soup.find_all("h2")[:5]] or \
                    [h.get_text(strip=True) for h in soup.find_all("h3")[:5]]
            headlines.append({"source": source, "headlines": found or ["⚠️ No headlines found"]})
        except Exception as e:
            headlines.append({"source": source, "error": str(e)})
    return headlines

# === AI Prompt ===
def generate_prompt():
    return f"""
📊 **Supply Chain Risk Assessment Report** 📊

🔹 **Industries Analyzed:** {', '.join(user_prefs['industries'])}
🔹 **Countries Included:** {', '.join(user_prefs['countries'])}
🔹 **Shipping Modes Considered:** {', '.join(user_prefs['shipping_modes'])}

💡 **Key Focus Areas**
- **Raw Materials:** Plastic resin, aluminum, and lithium supply trends.
- **Manufacturing Hubs:** China (Shenzhen, Dongguan), Vietnam (Ho Chi Minh), Indonesia.
- **Retail & E-commerce Impacts:** Amazon, Apple, Walmart, Best Buy.
- **Customs & Tariffs:** Recent US import/export policy updates affecting mobile accessories.

🚀 **Risk Categories:**
1️⃣ Geopolitical Risks
2️⃣ Logistics Risks
3️⃣ Economic Risks
4️⃣ Environmental Risks
5️⃣ Regulatory Risks
6️⃣ Technological Risks

✅ Exclude outdated pandemic-related risks. Provide forward-looking analysis.
"""

# === Risk Analysis ===
def assess_risks():
    freight_data = get_freight_rates()
    news_data = get_news_headlines()

    with open("freight_rates.json", "w") as f:
        json.dump(freight_data, f, indent=2)
    with open("supply_chain_news.json", "w") as f:
        json.dump(news_data, f, indent=2)

    try:
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "user", "content": generate_prompt()}],
            temperature=0.5,
            max_tokens=1000
        )
        summary = response.choices[0].message.content.strip()
        summary = summary.replace("\\n", "\n").replace("**", "").replace("\\", "")
    except Exception as e:
        summary = f"Error generating AI response: {e}"

    with open("categorized_risks.json", "w") as f:
        json.dump({"categorized_risks": summary}, f, indent=2)

    history_path = "risk_history.json"
    try:
        with open(history_path, "r") as f:
            history = json.load(f)
    except:
        history = {"history": []}

    history["history"].append({
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "risks": summary
    })
    history["history"] = history["history"][-10:]
    with open(history_path, "w") as f:
        json.dump(history, f, indent=2)

    return summary

# === Flask Routes ===
@app.route("/")
def home():
    return jsonify({"message": "Welcome to the Supply Chain Risk API! Try /api/risks or POST /api/run-analysis"})

@app.route("/api/risks", methods=["GET"])
def get_risks():
    if not os.path.exists("categorized_risks.json"):
        return jsonify({"error": "Risk data not found. Run analysis first."}), 404
    with open("categorized_risks.json") as f:
        return jsonify(json.load(f))

@app.route("/api/run-analysis", methods=["POST"])
def run_analysis():
    summary = assess_risks()
    return jsonify({"message": "✅ Analysis complete!", "summary": summary})

@app.route("/dashboard", methods=["GET"])
def dashboard():
    try:
        with open("categorized_risks.json", "r") as f:
            data = json.load(f)
    except FileNotFoundError:
        data = {"categorized_risks": "No risk data available. Run an analysis first."}

    return render_template("dashboard.html", risk_summary=data["categorized_risks"])

# === Launch Server ===
if __name__ == "__main__":
    app.run(debug=True)
