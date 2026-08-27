from flask import Flask, request, jsonify, render_template
import os

# Create Flask app
app = Flask(__name__)

# Set template folder path (important for Vercel)
template_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'templates')
app.template_folder = template_dir

@app.route('/')
def home():
    try:
        return render_template('index.html')
    except Exception as e:
        return f"Error: {str(e)}"

@app.route('/chat', methods=['POST'])
def chat():
    try:
        data = request.json
        user_message = data.get('message', '').strip()
        
        if not user_message:
            return jsonify({'error': 'Please enter a message'}), 400
        
        # Echo response (you can add Gemini AI here later)
        return jsonify({'response': f'Echo: {user_message}'})
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/health')
def health():
    return jsonify({
        'status': 'healthy',
        'template_folder': app.template_folder,
        'template_exists': os.path.exists(os.path.join(app.template_folder, 'index.html'))
    })

# Vercel handler
def handler(request, context):
    return app(request.environ, context.start_response)