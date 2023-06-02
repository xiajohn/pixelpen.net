
import os
from common.video.constants import Constants
from utils import Utils
import json
from dotenv import find_dotenv, load_dotenv
load_dotenv(find_dotenv('../.env'))

class MetadataManager():
    def __init__(self):
        self.video_metadata_file = "video/metadata.json"
        self.load_metadata()
        self.resources = {
            Constants.audio: "audio.mp3",
            Constants.video: "video.mp4",
            Constants.script: "script.txt",
            Constants.video_with_audio: "videoAudio.mp4",
            Constants.final_video: "videoAudioFinal.mp4",
            Constants.thumbnail: "thumbnail.txt",
            Constants.thumbnail_image: "thumbnail.jpg"
        }
    
    def load_metadata(self):
        if os.path.exists(self.video_metadata_file):
            with open(self.video_metadata_file, 'r') as f:
                self.metadata = json.load(f)
        else:
            self.metadata = {}

    def save_metadata(self):
        with open(self.video_metadata_file, 'w') as f:
            json.dump(self.metadata, f, indent=4)

    def check_metadata(self, resource_type, folder_path):
        file_path = os.path.join(folder_path, self.resources[resource_type])
        print(f'checking if {file_path} exists')
        exists = os.path.exists(file_path)
        if exists:
            print(f'{resource_type} exists')
        return exists

    def update_metadata(self, resource_type, query, resource_path):
        if query not in self.metadata:
            self.metadata[query] = {}
        self.metadata[query][resource_type] = resource_path
        self.save_metadata()

    


