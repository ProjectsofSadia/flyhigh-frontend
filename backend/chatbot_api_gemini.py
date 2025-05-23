import os
import flask
from flask import request, jsonify
from flask_cors import CORS
import google.generativeai as genai
from dotenv import load_dotenv
load_dotenv()
app = flask.Flask(__name__)
CORS(app)
api_key = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=api_key)
model = genai.GenerativeModel("gemini-pro")
chat = model.start_chat(history=[])

@app.route("/gemini", methods=["POST"])
def generate_response():
    try:
        data = request.get_json()
        prompt = data.get("message")
        response = chat.send_message(prompt)
        reply = response.text

        return jsonify({"response": reply})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)

