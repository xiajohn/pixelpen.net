from enum import Enum
import json
import os
class TopicType(Enum):
    TRANSACTIONAL = "TRANSACTIONAL"
    INFORMATIONAL = "INFORMATIONAL"


def load_json(file_path):
    current_dir = os.path.dirname(os.path.abspath(__file__))
    abs_file_path = os.path.join(current_dir, file_path)

    if not os.path.exists(abs_file_path):
        return {}  # Return an empty dictionary if the file doesn't exist
    else:
        with open(abs_file_path, "r") as file:
            return json.load(file)

def save_json(metadata, file_path):
    current_dir = os.path.dirname(os.path.abspath(__file__))
    abs_file_path = os.path.join(current_dir, file_path)

    with open(abs_file_path, "w") as file:
        json.dump(metadata, file, indent=2, ensure_ascii=False)