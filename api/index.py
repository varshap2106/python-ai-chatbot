from flask import Flask, request, jsonify, render_template 
import os 
import sys 
 
app = Flask(__name__) 
 
@app.route('/') 
def home(): 
    try: 
        return render_template('index.html') 
    except Exception as e: 
        return f"Error loading template: {e}" 
 
@app.route('/chat', methods=['POST']) 
def chat(): 
    try: 
        data = request.json 
        user_message = data.get('message', '').strip() 
        if not user_message: 
            return jsonify({'error': 'Please enter a message'}), 400 
        return jsonify({'response': 'Echo: ' + user_message}) 
    except Exception as e: 
        return jsonify({'error': str(e)}), 500 
 
@app.route('/health') 
def health(): 
    return jsonify({'status': 'healthy'}) 
 
def handler(request, context): 
    return app(request.environ, context.start_response) 
