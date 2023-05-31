from moviepy.editor import concatenate_videoclips, VideoFileClip, AudioFileClip, ImageClip, CompositeVideoClip, CompositeAudioClip
from common.metadata_manager import MetadataManager
import pixabay
import os
from common.video.constants import Constants
import requests
from moviepy.video.fx.all import fadeout
from moviepy.video.compositing.transitions import slide_in, slide_out
import logging
from common.video.audio_generator import AudioGenerator
from utils import Utils
from moviepy.video.io.ffmpeg_reader import FFMPEG_VideoReader
import json
from dotenv import find_dotenv, load_dotenv
from common.video.story_manager import StoryManager
load_dotenv(find_dotenv('../../.env'))
import warnings
import random
class VideoGenerator(AudioGenerator):
    def __init__(self, folder_name):
        self.px = pixabay.core(os.getenv("PIXABAY_KEY"))
        self.metadata_manager = MetadataManager()
        self.folder_name = folder_name
        self.story_manager = StoryManager(folder_name)

    def getVideo(self, length, query):
        path = f'{self.folder_name}/video.mp4'
        if self.metadata_manager.check_metadata(Constants.video, self.folder_name):
            return path

        url = f'https://pixabay.com/api/videos/?key={os.getenv("PIXABAY_KEY")}&q={query}'
        response = requests.get(url)
        data = {}
        if response.status_code == 200:
            data = response.json()  # parse the response as JSON
        else:
            print(f"Request failed with status code {response.status_code}")

        clips = []
        temp_files = [] # List to store temp video file paths

        videos = data["hits"]
        i = 0
        while i < length:
            temp_video_path = f'{query}{i}.mp4'
            Utils.download_file(videos[i]["videos"]["medium"]["url"], temp_video_path)
            clip = VideoFileClip(temp_video_path)
            clip = clip.resize(height=1920, width=1080)
            clips.append(clip)
            temp_files.append(temp_video_path) # Save temp file path
            i += 1

        final_clip = concatenate_videoclips(clips)
        final_clip.write_videofile(path, codec='libx264')
        for file in temp_files:
            if os.path.exists(file):
                os.remove(file)
        return path
    
    def addImage(self, video_path, image_path, start_time, duration):
        original = video_path[0:-4]
        final_location = original + "Final" + ".mp4"
        if self.metadata_manager.check_metadata(Constants.final_video, self.folder_name):
            return final_location
        video = VideoFileClip(video_path)
        image = (ImageClip(image_path)
                .set_duration(duration)
                .resize(width=620)
                .set_position(('center', 'center'))
                .set_start(start_time))
        print(video)
        print(image)
        final_clip = CompositeVideoClip([video, image])
        
        final_clip.write_videofile(f'{final_location}', codec='libx264')

        return f'{final_location}'

    def build_prompt(self, user_input):
        intro = f"In this audio, we're going to dive right into the exciting world of {user_input}.\n\n"
        script_prompt = f"{intro}We want to start the audio with a captivating hook. For instance, you could start with something like 'Imagine a world where {user_input} is at the forefront of every conversation.' But remember, that's just an example. We want you to come up with an original and engaging hook that fits the topic of {user_input}. After the hook, proceed directly into the informative content for a 1-minute audio script."
        return script_prompt


    def get_random_music_file(self, folder="music"):
        music_files = os.listdir(folder)  # Lists all files in the directory
        music_files = [f for f in music_files if f.endswith(".mp3")]  # Filter out non-music files
        if not music_files:
            raise Exception("No music files found in directory")
        return os.path.join(folder, random.choice(music_files))  # Picks a random file and returns the path

    
    def getScript(self, prompt):
        script_path = os.path.join(self.folder_name, 'script.txt')
        if self.metadata_manager.check_metadata(Constants.script, self.folder_name):
            with open(script_path, 'r') as f:
                text = f.read()
            return text
        text = self.generate_text(prompt)
        # Create directories if they don't exist
        os.makedirs(self.folder_name, exist_ok=True)
        
        # Save the text to a file in the given directory
        with open(os.path.join(self.folder_name, 'script.txt'), 'w') as f:
            f.write(text)
        return text

    def makeVideo(self, video):
        audio_prompt = video.get('audio')
        video_type = video.get('video')
        length = video.get('length')
        image_path = 'generated/alki-beach/image_data_1.jpg'
        self.folder_name = f'{Constants.video_file_path}{Utils.sanitize_folder_name(audio_prompt)}'
        music_path = self.get_random_music_file()

        logging.info(f"Generating script for {audio_prompt}...")
        prompt = self.build_prompt(audio_prompt)
        script = self.getScript(prompt)

        logging.info("Generating audio...")
        audio_path = self.getBadAudio(script, self.folder_name)

        logging.info(f"Generating {video_type} video...")
        video_path = self.getVideo(length, video_type)

        logging.info("Adding audio to video...")
        video_path = self.addAudio(video_path, audio_path, music_path, self.folder_name)
        print(f'video{video_path}')
        self.story_manager.addImageToVideo(video_path, image_path)
        logging.info("Video creation complete!")

def makeVideo():
    # Set up logging
    logging.basicConfig(level=logging.INFO)
    video_data = Utils.load_json("common/video/video_input.json")
    for category, category_data in video_data.items():
        for video in category_data['video']:
            audio_prompt = video.get('audio')
            vg = VideoGenerator(Utils.sanitize_folder_name(audio_prompt))
            vg.makeVideo(video)
