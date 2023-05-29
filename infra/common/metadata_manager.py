
import os
from common.video.constants import Constants
from common.utils import download_file
import json
from dotenv import find_dotenv, load_dotenv
load_dotenv(find_dotenv('../.env'))

class MetadataManager():
    def __init__(self):
        self.video_metadata_file = "video/metadata.json"
        self.load_metadata()
        self.metadata = {}
    
    def load_metadata(self):
        if os.path.exists(self.video_metadata_file):
            with open(self.video_metadata_file, 'r') as f:
                self.metadata = json.load(f)
        else:
            self.metadata = {}

    def save_metadata(self):
        with open(self.video_metadata_file, 'w') as f:
            json.dump(self.metadata, f, indent=4)

    def check_metadata(self, resource_type, query):
        return query in self.metadata and resource_type in self.metadata[query]

    def update_metadata(self, resource_type, query, resource_path):
        if query not in self.metadata:
            self.metadata[query] = {}
        self.metadata[query][resource_type] = resource_path
        self.save_metadata()

    


