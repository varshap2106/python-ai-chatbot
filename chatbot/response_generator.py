import requests
import json
from config import Config

class ResponseGenerator:
    def __init__(self):
        self.config = Config()
    
    def generate_response(self, user_input, intent_response=None):
        """Generate response based on intent or fallback"""
        if intent_response:
            return intent_response
        
        # Check if it's a programming question
        if self.is_programming_question(user_input):
            return self.get_programming_help(user_input)
        
        # Use OpenAI if available
        if self.config.USE_OPENAI and self.config.OPENAI_API_KEY:
            return self.get_openai_response(user_input)
        
        # Fallback response
        return self.get_fallback_response(user_input)
    
    def is_programming_question(self, text):
        """Check if the question is about programming"""
        programming_keywords = [
            'code', 'program', 'function', 'class', 'error', 'debug',
            'syntax', 'library', 'module', 'package', 'install', 'pip',
            'command', 'terminal', 'output', 'return', 'parameter',
            'argument', 'exception', 'try', 'except', 'finally',
            'list', 'dictionary', 'tuple', 'set', 'string', 'integer',
            'loop', 'for', 'while', 'if', 'else', 'elif'
        ]
        text_lower = text.lower()
        return any(keyword in text_lower for keyword in programming_keywords)
    
    def get_programming_help(self, user_input):
        """Provide help for programming questions"""
        common_help = {
            'print': "Use print() function to display output. Example: print('Hello World')",
            'input': "Use input() to get user input. Example: name = input('Enter name: ')",
            'if': "Use if-elif-else for conditional statements. Example: if x > 0: print('Positive')",
            'for loop': "Use for loop to iterate over sequences. Example: for i in range(5): print(i)",
            'while': "Use while loop for repetition. Example: while x < 10: x += 1",
            'function': "Define functions with def. Example: def greet(name): return f'Hello {name}'",
            'list': "Lists are ordered collections. Example: my_list = [1, 2, 3]",
            'dict': "Dictionaries store key-value pairs. Example: my_dict = {'key': 'value'}",
            'error': "Use try-except to handle errors. Example: try: x = 1/0 except ZeroDivisionError: print('Error')",
            'import': "Import modules with import statement. Example: import math",
            'class': "Define classes with class keyword. Example: class Person: def __init__(self, name): self.name = name"
        }
        
        text_lower = user_input.lower()
        for key, value in common_help.items():
            if key in text_lower:
                return value
        
        return "I'm here to help with Python programming! Could you be more specific about what you need?"
    
    def get_openai_response(self, user_input):
        """Get response from OpenAI API"""
        try:
            headers = {
                'Authorization': f'Bearer {self.config.OPENAI_API_KEY}',
                'Content-Type': 'application/json'
            }
            data = {
                'model': 'gpt-3.5-turbo',
                'messages': [
                    {'role': 'system', 'content': 'You are a Python programming assistant.'},
                    {'role': 'user', 'content': user_input}
                ],
                'max_tokens': 150
            }
            
            response = requests.post(
                'https://api.openai.com/v1/chat/completions',
                headers=headers,
                json=data,
                timeout=10
            )
            
            if response.status_code == 200:
                return response.json()['choices'][0]['message']['content']
        except:
            pass
        
        return None
    
    def get_fallback_response(self, user_input):
        """Return a fallback response when no specific match is found"""
        fallbacks = [
            "I'm not sure about that. Could you rephrase your question?",
            "That's an interesting question! Let me think... Could you be more specific?",
            "I specialize in Python programming. Feel free to ask me Python-related questions!",
            "I'm still learning! Could you ask about something specific in Python?"
        ]
        import random
        return random.choice(fallbacks)