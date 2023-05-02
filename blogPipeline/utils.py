from enum import Enum, auto
import json
class TopicType(Enum):
    TRANSACTIONAL = auto()
    INFORMATIONAL = auto()

def load_blog_metadata():
    with open("blog_metadata.json", "r") as file:
        return json.load(file)

def save_blog_metadata(metadata):
    with open("blog_metadata.json", "w") as file:
        json.dump(metadata, file, indent=2, ensure_ascii=False)