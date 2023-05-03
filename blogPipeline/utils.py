from enum import Enum, auto
import json
import os
class TopicType(Enum):
    TRANSACTIONAL = auto()
    INFORMATIONAL = auto()

def load_blog_metadata():
    file_path = "blog_metadata.json"
    if not os.path.exists(file_path):
        return {}  # Return an empty dictionary if the file doesn't exist
    else:
        with open(file_path, "r") as file:
            return json.load(file)

def save_blog_metadata(metadata):
    file_path = "blog_metadata.json"
    with open(file_path, "w") as file:
        json.dump(metadata, file, indent=2, ensure_ascii=False)
