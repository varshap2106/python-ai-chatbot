from flask import Flask, request, jsonify, render_template
import os
import sys

app = Flask(__name__)

# Set template folder path
template_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'templates')
app.template_folder = template_dir

# Initialize AI
ai_available = False
model = None

try:
    import google.generativeai as genai
    
    # Get API key from environment
    GEMINI_API_KEY = os.environ.get('GEMINI_API_KEY')
    
    if GEMINI_API_KEY and GEMINI_API_KEY != 'your-api-key-here':
        genai.configure(api_key=GEMINI_API_KEY)
        model = genai.GenerativeModel('models/gemini-2.5-flash')
        ai_available = True
        print("✅ Gemini AI configured successfully!")
    else:
        print("⚠️ No valid API key found")
        
except ImportError as e:
    print(f"❌ Import error: {e}")
except Exception as e:
    print(f"❌ Error: {e}")

@app.route('/')
def home():
    try:
        return render_template('index.html')
    except Exception as e:
        return f"Error loading template: {str(e)}"

@app.route('/chat', methods=['POST'])
def chat():
    try:
        data = request.json
        user_message = data.get('message', '').strip()
        
        if not user_message:
            return jsonify({'error': 'Please enter a message'}), 400
        
        # Get AI response
        if ai_available and model:
            try:
                prompt = f"""You are a helpful Python programming expert. Answer the user's question clearly with code examples when relevant. Keep responses concise but informative.

User question: {user_message}

Your response:"""
                
                response = model.generate_content(prompt)
                bot_response = response.text.strip()
                print(f"✅ AI Response generated for: {user_message[:50]}...")
                
            except Exception as e:
                bot_response = f"Error getting AI response: {str(e)}"
                print(f"❌ AI Error: {e}")
        else:
            # Fallback response
            bot_response = f"""🔧 AI is not configured. Here's why:

1. You need to add GEMINI_API_KEY in Vercel Environment Variables
2. Get a free API key from: https://makersuite.google.com/app/apikey
3. Add it in Vercel → Settings → Environment Variables
4. Redeploy your app

Your message was: {user_message}"""
            print("⚠️ Using fallback response - no API key")
        
        return jsonify({'response': bot_response})
        
    except Exception as e:
        print(f"❌ Chat error: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/health')
def health():
    return jsonify({
        'status': 'healthy',
        'gemini_configured': ai_available,
        'api_key_present': bool(os.environ.get('GEMINI_API_KEY')),
        'api_key_valid': bool(os.environ.get('GEMINI_API_KEY') and os.environ.get('GEMINI_API_KEY') != 'your-api-key-here')
    })

# Vercel handler
def handler(request, context):
    return app(request.environ, context.start_response)