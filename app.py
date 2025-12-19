from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # ✅ ALLOW frontend requests

@app.route("/")
def home():
    return "AI Page Quality Backend is running"

@app.route("/analyze", methods=["POST"])
def analyze_page():
    data = request.get_json() or {}
    url = data.get("url")

    if not url:
        return jsonify({"error": "URL is required"}), 400

    return jsonify({
        "status": "Backend connected successfully",
        "url_received": url
    })
