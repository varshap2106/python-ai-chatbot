import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()

# Configure
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
genai.configure(api_key=GEMINI_API_KEY)

# Test with best model
model = genai.GenerativeModel('models/gemini-2.5-flash')

try:
    response = model.generate_content("Say hello and introduce yourself as a Python assistant")
    print("✅ Connection successful!")
    print(f"Response: {response.text}")
except Exception as e:
    print(f"❌ Error: {e}")