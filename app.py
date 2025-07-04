from flask import Flask, render_template, jsonify, request, redirect
import json
import os
import subprocess
import requests

def send_notification_email(subject, message):
    MAILGUN_API_KEY = os.getenv("MAILGUN_API_KEY")
    MAILGUN_DOMAIN = os.getenv("MAILGUN_DOMAIN")
    RECIPIENT = "clark@case-mate.com"

    if not MAILGUN_API_KEY or not MAILGUN_DOMAIN:
        print("❌ Mailgun credentials missing.")
        return

    response = requests.post(
        f"https://api.mailgun.net/v3/{MAILGUN_DOMAIN}/messages",
        auth=("api", MAILGUN_API_KEY),
        data={
            "from": f"CLARQ Bot <no-reply@{MAILGUN_DOMAIN}>",
            "to": RECIPIENT,
            "subject": subject,
            "text": message
        }
    )
    print(f"📬 Notification email sent: {response.status_code}")
    
app = Flask(__name__)

# Auto-generate trends on app start (optional)
# subprocess.run(["python", "generate_risk_trends.py"])

# @app.route("/dashboard")
# def dashboard():
#    return render_template("dashboard.html")

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

@app.route("/intake", methods=["GET", "POST"])
def intake():
    if request.method == "POST":
        data = {
            "role": request.form.get("role"),
            "business_type": request.form.get("business_type"),
            "customers": request.form.get("customers"),
            "risks": request.form.get("risks"),
            "signals": request.form.get("signals"),
            "ideal_ops": request.form.get("ideal_ops")
        }

        with open("user_profile.json", "w") as f:
            json.dump(data, f, indent=2)

        return redirect("/dashboard")

    return render_template("intake.html")

@app.route("/refresh-headlines")
def refresh_headlines():
    key = request.args.get("key")
    debug = request.args.get("debug", "false").lower() == "true"

    if key != "clarqbolt55":
        return "⛔ Unauthorized", 401

    try:
        subprocess.run(["python3", "scripts/scrapers/fetch_splash247.py"], check=True)
        subprocess.run(["python3", "scripts/scrapers/supplychaindive_scraper.py"], check=True)
        subprocess.run(["python3", "scripts/merge_scraped_headlines.py"], check=True)

        if debug:
            subprocess.run(["python3", "scripts/processors/tag_and_score.py", "--debug"], check=True)
        else:
            subprocess.run(["python3", "scripts/processors/tag_and_score.py"], check=True)

        subprocess.run(["python3", "scripts/processors/generate_risk_blocks.py"], check=True)

        return "✅ Headlines refreshed successfully!"
    except Exception as e:
        return f"❌ Error: {str(e)}", 500

@app.route("/submit_pro_plan", methods=["POST"])
def submit_pro_plan():
    data = {
        "email": request.form.get("email"),
        "topics": request.form.get("topics"),
        "signals": request.form.get("signals"),
        "notes": request.form.get("notes")
    }

    print("📩 PRO PLAN SUBMISSION:")
    print(json.dumps(data, indent=2))

    with open("pro_submissions.json", "a") as f:
        f.write(json.dumps(data) + "\n")

    message = f"""
📥 New PRO Plan Submission

Email: {data['email']}
Topics: {data['topics']}
Signals: {data['signals']}
Notes: {data['notes']}
"""
    send_notification_email("New PRO Plan Signup", message)

    return redirect("/thank-you.html")


@app.route("/submit_elite_plan", methods=["POST"])
def submit_elite_plan():
    data = {
        "email": request.form.get("email"),
        "interests": request.form.get("interests"),
        "risks": request.form.get("risks"),
        "notes": request.form.get("notes")
    }

    print("📩 ELITE PLAN SUBMISSION:")
    print(json.dumps(data, indent=2))

    with open("elite_submissions.json", "a") as f:
        f.write(json.dumps(data) + "\n")

    message = f"""
🚨 New ELITE Plan Submission

Email: {data['email']}
Interests: {data['interests']}
Risks/Trends: {data['risks']}
Notes: {data['notes']}
"""
    send_notification_email("🔥 New ELITE Plan Signup", message)

    return redirect("/thank-you.html")
    
    
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
