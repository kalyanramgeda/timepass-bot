from flask import Flask, request, jsonify
from flask_cors import CORS
import requests

app = Flask(__name__)
CORS(app)

# Replace with your actual Gemini API key
GEMINI_API_KEY = "enter your api key because it not free "
GEMINI_API_URL = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={GEMINI_API_KEY}"

@app.route("/chat", methods=["POST"])
def chat():
    data = request.json
    user_message = data.get("message", "")

    headers = {
        "Content-Type": "application/json"
    }

    body = {
        "contents": [
            {
                "parts": [
                    {"text": user_message}
                ]
            }
        ]
    }

    response = requests.post(GEMINI_API_URL, headers=headers, json=body)
    
    if response.status_code == 200:
        result = response.json()
        try:
            reply = result["candidates"][0]["content"]["parts"][0]["text"]
        except (KeyError, IndexError):
            reply = "Oops! Couldn't understand the response."
    else:
        reply = f"Error: {response.status_code} - {response.text}"

    return jsonify({"response": reply})

if __name__ == "__main__":
    app.run(debug=True)
