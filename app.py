from flask import Flask, render_template, jsonify
import json

from flask import Flask, render_template, request, redirect
import json

app = Flask(__name__)

@app.route("/dashboard")
def dashboard():
    with open("risk_blocks_transformed.json") as f:
        risk_blocks = json.load(f)

    with open("risk_trends.json") as f:
        risk_trends = json.load(f)

    summary_block = next((b for b in risk_blocks if b.get("type") == "summary"), None)
    rumor_blocks = [b for b in risk_blocks if b.get("type") == "rumor"]
    normal_blocks = [b for b in risk_blocks if b.get("type") not in ("summary", "rumor")]

    return render_template("dashboard.html",
                           summary_block=summary_block,
                           risk_blocks=normal_blocks,
                           rumor_blocks=rumor_blocks,
                           risk_trends=risk_trends)

@app.route('/api/risks')
def api_risks():
    try:
        with open("risk_blocks_transformed.json") as f:
            data = json.load(f)
        print("API /api/risks served successfully")  # 🧠
        return jsonify(data)
    except Exception as e:
        print(f"API Error: {e}")  # 🧠
        return jsonify({"error": str(e)}), 500

@app.route("/setup", methods=["GET", "POST"])
def setup():
    if request.method == "POST":
        data = {
            "business_type": request.form.get("business_type"),
            "countries": request.form.get("countries"),
            "risks": request.form.getlist("risks"),
            "signals": request.form.get("signals")
        }

        with open("user_profile.json", "w") as f:
            json.dump(data, f, indent=2)

        return redirect("/dashboard")

    return render_template("setup.html")

import os

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))  # Render provides PORT, fallback for local testing
    app.run(host="0.0.0.0", port=port)
