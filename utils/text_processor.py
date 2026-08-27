import re
import string

class TextProcessor:
    @staticmethod
    def clean_text(text):
        """Clean and normalize text"""
        # Convert to lowercase
        text = text.lower()
        # Remove extra whitespace
        text = ' '.join(text.split())
        # Remove punctuation
        text = text.translate(str.maketrans('', '', string.punctuation))
        return text
    
    @staticmethod
    def extract_keywords(text):
        """Extract keywords from text"""
        # Remove stop words (simple implementation)
        stop_words = {'the', 'a', 'an', 'is', 'are', 'was', 'were', 'for', 'on', 'at', 'to', 'in', 'with', 'by'}
        words = text.lower().split()
        keywords = [word for word in words if word not in stop_words and len(word) > 2]
        return keywords
    
    @staticmethod
    def tokenize_sentences(text):
        """Split text into sentences"""
        sentences = re.split(r'[.!?]+', text)
        return [s.strip() for s in sentences if s.strip()]