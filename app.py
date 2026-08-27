import os
from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv
import google.generativeai as genai

# Load environment variables
load_dotenv()

app = Flask(__name__)

# Configure Gemini
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
genai.configure(api_key=GEMINI_API_KEY)

# Use the latest model from your list
model = genai.GenerativeModel('models/gemini-2.5-flash')

# Conversation history
chat_history = []

def get_gemini_response(user_message):
    """Get response from Gemini AI"""
    try:
        prompt = f"""You are a helpful Python programming expert. Answer clearly with code examples when helpful.

Question: {user_message}

Answer:"""
        
        response = model.generate_content(prompt)
        return response.text.strip()
    
    except Exception as e:
        return f"Error: {str(e)}"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    data = request.json
    user_message = data.get('message', '').strip()
    
    if not user_message:
        return jsonify({'error': 'Please enter a message'}), 400
    
    bot_response = get_gemini_response(user_message)
    
    chat_history.append({
        'user': user_message,
        'bot': bot_response
    })
    
    return jsonify({
        'response': bot_response,
        'history': chat_history
    })

@app.route('/clear', methods=['POST'])
def clear_history():
    global chat_history
    chat_history = []
    return jsonify({'status': 'History cleared'})

if __name__ == '__main__':
    if not os.path.exists('templates'):
        os.makedirs('templates')
    
    print("🚀 Python AI Assistant is running!")
    print("🌐 Open: http://localhost:5000")
    app.run(debug=True, host='0.0.0.0', port=5000)