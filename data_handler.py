import json
import os

class DataHandler:
    """Handles loading and saving data to and from JSON files."""

    @staticmethod
    def save_to_json_file(data, filename: str):
        """Saves data to a JSON file."""
        with open(filename, "w", encoding="utf-8") as file:
            json.dump(data, file, indent=4)
        print(f"Data successfully saved to {filename}.")

    @staticmethod
    def load_from_json_file(filename: str):
        """Loads data from a JSON file and returns the appropriate structure based on the file type."""
        if not os.path.exists(filename):
            print(f"{filename} does not exist. Returning a default structure.")
            return DataHandler._get_default_structure(filename)

        try:
            with open(filename, "r", encoding="utf-8") as file:
                content = file.read().strip()
                if not content:
                    print(f"{filename} is empty. Returning a default structure.")
                    return DataHandler._get_default_structure(filename)
                return json.loads(content)
        except json.JSONDecodeError as e:
            print(f"Error decoding JSON in {filename}: {e}")
            return DataHandler._get_default_structure(filename)

    @staticmethod
    def _get_default_structure(filename: str):
        """Returns the default structure based on the file type."""
        if "user" in filename.lower():
            return {"users": []}  # Default structure for user data
        elif "data" in filename.lower():
            return {"products": [], "categories": []}  # Default structure for product and category data
        else:
            print("Unknown file type. Returning an empty dictionary.")
            return {}
