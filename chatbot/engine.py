from .intent_processor import IntentProcessor
from .response_generator import ResponseGenerator
from utils.text_processor import TextProcessor
import re

class ChatbotEngine:
    def __init__(self, knowledge_base_path):
        self.intent_processor = IntentProcessor(knowledge_base_path)
        self.response_generator = ResponseGenerator()
        self.text_processor = TextProcessor()
        self.greeting_patterns = ['hello', 'hi', 'hey', 'good morning', 'good afternoon']
        self.farewell_patterns = ['bye', 'goodbye', 'exit', 'quit', 'see you']
    
    def get_response(self, user_input):
        """Main method to get chatbot response"""
        if not user_input or not user_input.strip():
            return "Please enter a question or message."
        
        user_input = user_input.strip()
        
        # Check for greetings
        if self.is_greeting(user_input):
            return self.intent_processor.get_greeting_response()
        
        # Check for farewell
        if self.is_farewell(user_input):
            return self.intent_processor.get_farewell_response()
        
        # Try to match with knowledge base
        intent_response = self.intent_processor.get_intent(user_input)
        
        # Generate response
        response = self.response_generator.generate_response(user_input, intent_response)
        
        return response
    
    def is_greeting(self, text):
        """Check if input is a greeting"""
        text_lower = text.lower()
        return any(pattern in text_lower for pattern in self.greeting_patterns)
    
    def is_farewell(self, text):
        """Check if input is a farewell"""
        text_lower = text.lower()
        return any(pattern in text_lower for pattern in self.farewell_patterns)