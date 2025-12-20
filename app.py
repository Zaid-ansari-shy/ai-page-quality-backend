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

    hf_key = os.getenv("HF_API_KEY")
    if not hf_key:
        return jsonify({"error": "HF_API_KEY not set"}), 500

    API_URL = "https://api-inference.huggingface.co/models/mistralai/Mistral-7B-Instruct-v0.2"
    headers = {
        "Authorization": f"Bearer {hf_key}",
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
        "inputs": prompt,
        "parameters": {
            "max_new_tokens": 500,
            "temperature": 0.2
        }
    }

    response = requests.post(API_URL, headers=headers, json=payload)

    if response.status_code != 200:
        return jsonify({
            "error": "Hugging Face API error",
            "details": response.text
        }), 500

    output_text = response.json()[0]["generated_text"]

    try:
        parsed = json.loads(output_text)
        return jsonify(parsed)
    except Exception:
        return jsonify({
            "error": "Model did not return valid JSON",
            "raw": output_text
        })
