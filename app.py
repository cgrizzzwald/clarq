from flask import Flask, render_template, jsonify
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

if __name__ == "__main__":
    app.run(port=10000)
