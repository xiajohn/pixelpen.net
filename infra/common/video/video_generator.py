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
load_dotenv(find_dotenv('../../.env'))
import warnings

class VideoGenerator(AudioGenerator):
    def __init__(self):
        self.px = pixabay.core(os.getenv("PIXABAY_KEY"))
        self.metadata_manager = MetadataManager()
        self.video_exists = True

    def getVideo(self, length, query, folder_name):
        path = f'{folder_name}/video.mp4'
        if self.metadata_manager.check_metadata(Constants.video, folder_name):
            return path
        self.video_exists = False

        url = f'https://pixabay.com/api/videos/?key={os.getenv("PIXABAY_KEY")}&q={query}'
        response = requests.get(url)
        data = {}
        if response.status_code == 200:
            data = response.json()  # parse the response as JSON
        else:
            print(f"Request failed with status code {response.status_code}")

        clips = []

        videos = data["hits"]
        i = 0
        while i < length:
            Utils.download_file(videos[i]["videos"]["medium"]["url"], f'{query}{i}.mp4')

            clip = VideoFileClip(f'{query}{i}.mp4')
            clip = clip.resize(height=1920, width=1080)
            clips.append(clip)
            i += 1
        final_clip = concatenate_videoclips(clips)
        final_clip.write_videofile(path, codec='libx264')
        self.metadata_manager.update_metadata(folder_name, Constants.video, Utils.sanitize_folder_name(path))
        return path
    
    def addImage(self, video_path, image_path, start_time, duration):
        video = VideoFileClip(video_path)
        image = (ImageClip(image_path)
                .set_duration(duration)
                .resize(width=620)
                .set_position(('center', 'center'))
                .set_start(start_time))
        print(video)
        print(image)
        final_clip = CompositeVideoClip([video, image])

        final_clip.write_videofile(f'{video_path}', codec='libx264')

        return f'{video_path}'

    def build_prompt(self, user_input):
        intro = f"In this video, we're going to dive right into the exciting world of {user_input}.\n\n"
        script_prompt = f"{intro}We want to start the video with a captivating hook. For instance, you could start with something like 'Imagine a world where {user_input} is at the forefront of every conversation.' But remember, that's just an example. We want you to come up with an original and engaging hook that fits the topic of {user_input}. After the hook, proceed directly into the informative content."
        return script_prompt

    def searchMusic(query):
        api_key = 'your_pixabay_api_key'
        url = f'https://pixabay.com/api/?key={api_key}&q={query}&media=music'
        response = requests.get(url).json()
        print(response)
        if 'hits' in response:
            for hit in response['hits']:
                print(hit['pageURL'])

    
    def getScript(self, prompt, folder_path):
        script_path = os.path.join(folder_path, 'script.txt')
        if self.metadata_manager.check_metadata(Constants.script, folder_path):
            with open(script_path, 'r') as f:
                text = f.read()
            return text
        self.video_exists = False
        text = self.generate_text(prompt)
        # Create directories if they don't exist
        os.makedirs(folder_path, exist_ok=True)
        
        # Save the text to a file in the given directory
        with open(os.path.join(folder_path, 'script.txt'), 'w') as f:
            f.write(text)
        return text

    def makeVideos(self, video_data):
        logging.basicConfig(level=logging.INFO)

        for category, category_data in video_data.items():
            for video in category_data['video']:
                audio_prompt = video.get('audio')
                video_type = video.get('video')
                
                image_path = 'generated/alki-beach/image_data_1.jpg'
                folder_name = f'{Constants.video_file_path}{Utils.sanitize_folder_name(audio_prompt)}'
                music_path = f'{folder_name}/relaxed-vlog-night-street-131746.mp3'
                logging.info(f"Generating script for {audio_prompt}...")
                prompt = self.build_prompt(audio_prompt)
                script = self.getScript(prompt, folder_name)
                logging.info("Generating audio...")

                if not self.metadata_manager.check_metadata(Constants.audio, folder_name):
                    self.video_exists = False
                    
                audio_path = self.getBadAudio(script, folder_name)
                logging.info(f"Generating {video_type} video...")
                video_path = self.getVideo(3, video_type, folder_name)

                logging.info("Adding audio to video...")
                self.addAudio(video_path, audio_path, music_path, folder_name)
                #if not self.video_exists:
                    
                self.addImage(video_path, image_path, start_time=1, duration=13)
                logging.info("Video creation complete!")

def makeVideo():
    # Set up logging
    logging.basicConfig(level=logging.INFO)
    vg = VideoGenerator()
    vg.makeVideos(Utils.load_json("common/video/video_input.json"))
    for i in range(3):
        video_file_name = f'space{i}.mp4'
        if os.path.exists(video_file_name):
            os.remove(video_file_name)