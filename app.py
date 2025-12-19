from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import json
from openai import OpenAI

app = Flask(__name__)
CORS(app)

@app.route("/")
def home():
    return "AI Page Quality Backend is running"

@app.route("/analyze", methods=["POST"])
def analyze_page():
    data = request.get_json() or {}
    url = data.get("url")

    if not url:
        return jsonify({"error": "URL is required"}), 400

    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        return jsonify({"error": "OPENAI_API_KEY not set"}), 500

    client = OpenAI(api_key=api_key)

    prompt = f"""
You are a Search Quality Rater assistant.

Analyze the webpage at this URL:
{url}

Respond ONLY in valid JSON with this exact structure:
{{
  "purpose": "...",
  "ymyl": "...",
  "reputation": "...",
  "mc_quality": "...",
  "eeat": "...",
  "overall_pq": "..."
}}
"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.2
    )

    ai_text = response.choices[0].message.content.strip()

    try:
        parsed = json.loads(ai_text)
        return jsonify(parsed)
    except Exception:
        return jsonify({
            "error": "AI returned invalid JSON",
            "raw": ai_text
        })
