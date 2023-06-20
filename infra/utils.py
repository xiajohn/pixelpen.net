from enum import Enum
import json
import os
import requests
import glob
class TopicType(Enum):
    TRANSACTIONAL = "TRANSACTIONAL"
    INFORMATIONAL = "INFORMATIONAL"


class Utils:
    def __init__(self):
        pass
    @staticmethod
    def load_json(file_path):
        base_dir = os.path.dirname(os.path.abspath(__file__))
        abs_file_path = os.path.join(base_dir, file_path)
        if not os.path.exists(abs_file_path):
            return {}  # Return an empty dictionary if the file doesn't exist
        else:
            with open(abs_file_path, "r") as file:
                return json.load(file)
    @staticmethod
    def save_json(metadata, file_path):
        base_dir = os.path.dirname(os.path.abspath(__file__))
        abs_file_path = os.path.join(base_dir, file_path)
        with open(abs_file_path, "w") as file:
            json.dump(metadata, file, indent=2, ensure_ascii=False)
    @staticmethod
    def download_file(url, file_path):
        base_dir = os.path.dirname(os.path.abspath(__file__))
        abs_file_path = os.path.join(base_dir, file_path)
        os.makedirs(os.path.dirname(abs_file_path), exist_ok=True)
        response = requests.get(url)
        with open(abs_file_path, 'wb') as f:
            f.write(response.content)
        print(f'download and saving file to {file_path}')
        return file_path
    @staticmethod
    def sanitize_folder_name(name):
        name = name.replace(':', '').replace(' ', '-')
        invalid_chars = '\/:*?"<>|'
        sanitized_name = ''.join(
            c if c not in invalid_chars else '_' for c in name)
        return sanitized_name
    @staticmethod
    def remove_mp4_files(directory):
    # Get a list of all the .mp4 files in the directory
        mp4_files = glob.glob(os.path.join(directory, "*.mp4"))
        print(os.path.join(directory, "*.mp4"))
        # Iterate over the list of filepaths & remove each file.
        for file in mp4_files:
            try:
                os.remove(file)
                print(f"File {file} has been removed successfully")
            except Exception as e:
                print(f"Error occurred while deleting file {file}. Reason: {str(e)}")