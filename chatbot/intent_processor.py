import re
import string
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import json

class IntentProcessor:
    def __init__(self, knowledge_base_path):
        self.knowledge_base = self.load_knowledge_base(knowledge_base_path)
        self.vectorizer = TfidfVectorizer(stop_words='english')
        self.patterns = []
        self.responses = []
        self.prepare_patterns()
    
    def load_knowledge_base(self, path):
        try:
            with open(path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            print(f"Knowledge base file not found at {path}")
            return {}
    
    def prepare_patterns(self):
        """Prepare patterns and responses from knowledge base"""
        for category, items in self.knowledge_base.items():
            for item in items:
                for pattern in item['pattern']:
                    self.patterns.append(pattern.lower())
                    self.responses.append(item['response'])
        
        if self.patterns:
            self.vectorizer.fit(self.patterns)
    
    def preprocess_text(self, text):
        """Clean and preprocess text"""
        # Convert to lowercase
        text = text.lower()
        # Remove punctuation
        text = text.translate(str.maketrans('', '', string.punctuation))
        return text
    
    def get_intent(self, user_input):
        """Determine the intent of user input"""
        if not self.patterns:
            return None
        
        user_input = self.preprocess_text(user_input)
        
        # Check for exact or partial matches first
        for category, items in self.knowledge_base.items():
            for item in items:
                for pattern in item['pattern']:
                    if pattern in user_input or user_input in pattern:
                        return item['response']
        
        # Use TF-IDF and cosine similarity for fuzzy matching
        try:
            user_vector = self.vectorizer.transform([user_input])
            pattern_vectors = self.vectorizer.transform(self.patterns)
            similarities = cosine_similarity(user_vector, pattern_vectors)[0]
            max_similarity = np.max(similarities)
            
            if max_similarity > 0.3:  # Threshold for matching
                best_match_index = np.argmax(similarities)
                return self.responses[best_match_index]
        except:
            pass
        
        return None
    
    def get_greeting_response(self):
        """Return a greeting response"""
        return "Hello! How can I help you with Python today?"
    
    def get_farewell_response(self):
        """Return a farewell response"""
        return "Goodbye! Keep coding in Python!"