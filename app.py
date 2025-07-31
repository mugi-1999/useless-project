from flask import Flask, request, jsonify
from flask_cors import CORS
import google.generativeai as genai
import os
from dotenv import load_dotenv  # Used to load environment variables from .env file

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# --- Configure Gemini API ---
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY not found in environment variables. Please set it in a .env file or your system.")

genai.configure(api_key=GEMINI_API_KEY)

MODEL_NAME = "gemini-1.5-flash"
SYSTEM_INSTRUCTION = """
You are 'The Reality Roaster', an AI whose sole purpose is to deliver harsh but funny reality checks and sarcastic roasts about people's choices. 
Be direct, witty, and slightly cynical, but aim to make them think and reflect. 
When given a choice or a situation, identify its flaws, impracticalities, or overlooked downsides with sharp humor. 
Use a biting, dry wit. Do not be overly polite or gentle.
Conclude your response with a clear "Reality check:" followed by practical, often uncomfortable, advice or questions designed to make the user confront the logical consequences of their choice.
Keep the language natural, like a smart, sarcastic friend giving tough love.
"""

# --- Initialize Gemini Model ---
model = genai.GenerativeModel(
    model_name=MODEL_NAME,
    system_instruction=SYSTEM_INSTRUCTION
)

# ✅ NEW: Home route to prevent 404 when visiting base URL
@app.route('/')
def home():
    return "✅ Reality Roaster API is live. Use POST /audit to roast your life choices."

@app.route('/audit', methods=['POST'])
def audit_choice():
    data = request.json
    user_choice = data.get('choice', '')

    if not user_choice:
        return jsonify({"audit_result": "Even silence reveals poor judgment. Try again."}), 400

    try:
        response_stream = model.generate_content(user_choice, stream=True)
        full_response_text = ""
        for chunk in response_stream:
            full_response_text += chunk.text

        return jsonify({"audit_result": full_response_text})

    except Exception as e:
        print(f"Error calling Gemini API: {e}")
        return jsonify({"audit_result": "Error: My cosmic judgment circuits are malfunctioning. Blame the universe, not your choices."}), 500

if __name__ == '__main__':
    app.run(debug=True)
