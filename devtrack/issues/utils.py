import os, json, threading
class JSONFileHandler:
    """A reusable class to safely read, write, and modify JSON files."""
    
    def __init__(self, filepath: str) -> None:
        self.filepath = filepath
        self._lock = threading.Lock()

    def read(self):
        """Reads and returns the JSON file data. Returns an empty dict if the file is missing or invalid."""
        if not os.path.exists(self.filepath):
            print(f"Warning: File '{self.filepath}' not found. Returning empty dictionary.")
            return []
        
        try:
            with open(self.filepath, 'r', encoding='utf-8') as file:
                return json.load(file)
        except json.JSONDecodeError:
            print(f"Error: '{self.filepath}' contains malformed JSON data. Returning empty dictionary.")
            return []
        except Exception as e:
            print(f"An unexpected error occurred while reading: {e}")
            return []

    def write(self, data) -> bool:
        """Writes a dictionary entirely to the JSON file, formatting it cleanly."""
        try:
            # Ensure the directory structure exists
            directory = os.path.dirname(self.filepath)
            if directory and not os.path.exists(directory):
                os.makedirs(directory, exist_ok=True)
                
            with open(self.filepath, 'w', encoding='utf-8') as file:
                json.dump(data, file, indent=4, ensure_ascii=False)
            return True
        except Exception as e:
            print(f"An error occurred while writing: {e}")
            return False
