import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()

# Configure Gemini
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
genai.configure(api_key=GEMINI_API_KEY)

# List all available models
print("Available Gemini models:")
for model in genai.list_models():
    print(f"- {model.name}")