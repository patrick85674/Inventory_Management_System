import json
import os

class DataHandler:
    """Handles loading and saving data to and from a JSON file."""

    @staticmethod
    def save_to_json_file(data, filename: str):
        """Saves data to a JSON file."""
        with open(filename, "w", encoding="utf-8") as file:
            json.dump(data, file, indent=4)
        print(f"Data successfully saved to {filename}.")

    @staticmethod
    def load_from_json_file(filename: str):
        """Loads data from a JSON file."""
        if not os.path.exists(filename):
            print(f"{filename} does not exist. Returning an empty dictionary.")
            return {"products": [], "categories": []}
        
        with open(filename, "r", encoding="utf-8") as file:
            return json.load(file)
