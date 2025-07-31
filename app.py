from flask import Flask, request, jsonify, render_template # <-- ADDED render_template
from flask_cors import CORS
import google.generativeai as genai
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)
CORS(app) # Enable CORS for all routes

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

model = genai.GenerativeModel(
    model_name=MODEL_NAME,
    system_instruction=SYSTEM_INSTRUCTION
)

# --- NEW ROUTE: Serve the HTML file when the root URL is accessed ---
@app.route('/')
def index():
    # Flask will look for 'useless.html' inside a 'templates' folder
    return render_template('useless.html') # <-- CHANGED FROM 'index.html' TO 'useless.html'

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