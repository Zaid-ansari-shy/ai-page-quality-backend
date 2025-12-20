from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import requests
import json

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

    groq_key = os.getenv("GROQ_API_KEY")
    if not groq_key:
        return jsonify({"error": "GROQ_API_KEY not set"}), 500

    API_URL = "https://api.groq.com/openai/v1/chat/completions"

    headers = {
        "Authorization": f"Bearer {groq_key}",
        "Content-Type": "application/json"
    }

    prompt = f"""
You are a Search Quality Rater assistant.

Analyze the webpage at this URL:
{url}

Respond ONLY in valid JSON:
{{
  "purpose": "...",
  "ymyl": "...",
  "reputation": "...",
  "mc_quality": "...",
  "eeat": "...",
  "overall_pq": "..."
}}
"""

    payload = {
        "model": "llama3-8b-8192",
        "messages": [
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.2,
        "max_tokens": 600
    }

    response = requests.post(API_URL, headers=headers, json=payload)

    if response.status_code != 200:
        return jsonify({
            "error": "Groq API error",
            "details": response.text
        }), 500

    ai_text = response.json()["choices"][0]["message"]["content"]

    try:
        parsed = json.loads(ai_text)
        return jsonify(parsed)
    except Exception:
        return jsonify({
            "error": "AI returned invalid JSON",
            "raw": ai_text
        })
