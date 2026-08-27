import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class Config:
    # OpenAI API Key (if you want to use GPT)
    OPENAI_API_KEY = os.getenv('OPENAI_API_KEY', '')
    
    # Model settings
    USE_OPENAI = False  # Set to True if you have API key
    
    # Knowledge base path
    KNOWLEDGE_BASE_PATH = 'knowledge_base.json'
    FAQ_PATH = 'data/python_faqs.json'
    
    # Chat settings
    MAX_RESPONSE_LENGTH = 500
    SIMILARITY_THRESHOLD = 0.6