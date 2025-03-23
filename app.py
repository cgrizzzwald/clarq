from flask import Flask, jsonify
import json

app = Flask(__name__)

@app.route('/api/risk', methods=['GET'])
def get_risk_data():
    try:
        with open("categorized_risks.json", "r") as f:
            risk_data = json.load(f)

        # Convert risks into a structured dictionary
        formatted_data = {"categorized_risks": []}

        # Parse the existing risk string into a clean structure
        for line in risk_data["categorized_risks"].split("\n"):
            if "**" in line:  # Detects category headers
                current_category = line.replace("**", "").strip()
                formatted_data["categorized_risks"].append({"category": current_category, "risks": []})
            elif "Severity Score" in line:  # Detects actual risk entries
                formatted_data["categorized_risks"][-1]["risks"].append(line.strip())

        return jsonify(formatted_data), 200
    except FileNotFoundError:
        return jsonify({"error": "Risk data not found. Run the analysis script first."}), 404

if __name__ == '__main__':
    app.run(debug=True)
