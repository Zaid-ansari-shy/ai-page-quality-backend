from flask import Flask, request, jsonify
import os
from openai import OpenAI

app = Flask(__name__)

# Read API key securely from environment variable
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

@app.route("/", methods=["GET"])
def home():
    return "AI Page Quality Backend is running"

@app.route("/analyze", methods=["POST"])
def analyze_page():
    data = request.get_json()
    url = data.get("url")

    if not url:
        return jsonify({"error": "URL is required"}), 400

    prompt = f"""
You are a Search Quality Rater assistant.

Analyze the webpage at this URL:
{url}

Answer these Page Quality questions:
1. True purpose of the page
2. Harmful or deceptive (Yes/No/Maybe)
3. YMYL classification and category
4. Reputation of responsible parties
5. Main content quality
6. E-E-A-T evaluation
7. Overall Page Quality rating (Lowest to Highest)

Give clear, structured answers.
"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3
    )

    return jsonify({
        "analysis": response.choices[0].message.content
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)

