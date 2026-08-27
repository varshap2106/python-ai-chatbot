import json
import os

class FileHandler:
    @staticmethod
    def load_json(file_path):
        """Load JSON file"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            print(f"File not found: {file_path}")
            return None
        except json.JSONDecodeError:
            print(f"Invalid JSON in file: {file_path}")
            return None
    
    @staticmethod
    def save_json(data, file_path):
        """Save data to JSON file"""
        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            return True
        except Exception as e:
            print(f"Error saving file: {e}")
            return False
    
    @staticmethod
    def file_exists(file_path):
        """Check if file exists"""
        return os.path.exists(file_path)