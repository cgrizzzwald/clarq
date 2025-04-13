from flask import Flask, render_template, jsonify, request, redirect
import json
import os
import subprocess

app = Flask(__name__)

# Auto-generate trends on app start (optional)
subprocess.run(["python", "generate_risk_trends.py"])

@app.route("/dashboard")
def dashboard():
    return render_template("dashboard.html")

@app.route("/api/risks")
def api_risks():
    try:
        with open("risk_blocks_transformed.json") as f:
            data = json.load(f)
        return jsonify(data)
    except Exception as e:
        print(f"API Error: {e}")
        return jsonify({"error": str(e)}), 500

@app.route("/api/headlines")
def api_headlines():
    try:
        with open("data/merged_articles.json") as f:
            data = json.load(f)
        return jsonify(data)
    except Exception as e:
        print(f"Headlines API Error: {e}")
        return jsonify([]), 500

@app.route("/setup", methods=["GET", "POST"])
def setup():
    if request.method == "POST":
        data = {
            "business_type": request.form.get("business_type"),
            "countries": request.form.get("countries"),
            "risks": request.form.getlist("risks"),
            "signals": request.form.get("signals"),
            "ideal_ops": request.form.get("ideal_ops"),
            "monitored_threats": request.form.get("monitored_threats")
        }
        with open("user_profile.json", "w") as f:
            json.dump(data, f, indent=2)
        return redirect("/dashboard")
    return render_template("setup.html")

@app.route("/refresh-headlines")
def refresh_headlines():
    key = request.args.get("key")
    if key != "clarqbolt55":
        return "⛔ Unauthorized", 401
    try:
        subprocess.run(["python3", "scripts/scrapers/fetch_splash247.py"], check=True)
        subprocess.run(["python3", "scripts/merge_scraped_headlines.py"], check=True)
        return "✅ Headlines refreshed successfully!"
    except Exception as e:
        return f"❌ Error: {str(e)}", 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
