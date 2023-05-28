from moviepy.editor import concatenate_videoclips, VideoFileClip, AudioFileClip, ImageClip, CompositeVideoClip, CompositeAudioClip

import pixabay
import os
from common.video.constants import Constants
import requests
from moviepy.video.fx.all import fadeout
from moviepy.video.compositing.transitions import slide_in, slide_out
import logging
from common.video.audio_generator import AudioGenerator
from common.utils import download_file
from moviepy.video.io.ffmpeg_reader import FFMPEG_VideoReader
import json
from dotenv import find_dotenv, load_dotenv
load_dotenv(find_dotenv('../../.env'))
import warnings
warnings.filterwarnings("ignore", category=UserWarning, module=FFMPEG_VideoReader.__module__)
class MetadataManager():
    def __init__(self):
        self.px = pixabay.core(os.getenv("PIXABAY_KEY"))
        self.metadata_file = "metadata.json"
        self.load_metadata()
    
    def load_metadata(self):
        if os.path.exists(self.metadata_file):
            with open(self.metadata_file, 'r') as f:
                self.metadata = json.load(f)
        else:
            self.metadata = {}

    def save_metadata(self):
        with open(self.metadata_file, 'w') as f:
            json.dump(self.metadata, f, indent=4)

    def check_metadata(self, resource_type, query):
        return query in self.metadata and resource_type in self.metadata[query]

    def update_metadata(self, resource_type, query, resource_path):
        if query not in self.metadata:
            self.metadata[query] = {}
        self.metadata[query][resource_type] = resource_path
        self.save_metadata()

    


