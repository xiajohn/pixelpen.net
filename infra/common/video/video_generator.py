from moviepy.editor import concatenate_videoclips, VideoFileClip, AudioFileClip, ImageClip, CompositeVideoClip, CompositeAudioClip
from common.metadata_manager import MetadataManager
import pixabay
import os
from common.constants import Constants
import requests
from moviepy.video.fx.all import fadeout
from moviepy.video.compositing.transitions import slide_in, slide_out
import logging
from common.video.audio_generator import AudioGenerator
from utils import Utils
from moviepy.video.io.ffmpeg_reader import FFMPEG_VideoReader
from common.makememe.generator.design.image_manager import Image_Manager
import json
from dotenv import find_dotenv, load_dotenv
from common.video.story_manager import StoryManager
from datetime import datetime
load_dotenv(find_dotenv('../../.env'))
import warnings
import random
import re
from collections import deque
from common.content_generator import ContentGenerator
from clients.midjourney_api import MidjourneyApi
from common.video.video_uploader import upload_video
class VideoGenerator(ContentGenerator):
    def __init__(self, folder_name):
        self.px = pixabay.core(os.getenv("PIXABAY_KEY"))
        self.metadata_manager = MetadataManager()
        self.folder_name = folder_name
        self.story_manager = StoryManager(folder_name)
        self.audio_duration = None
        self.audio_generator = AudioGenerator()

    def script_to_list(self, script):
        sentences = [sentence.strip() for sentence in re.split('([.!?])', script) if sentence.strip()]
        formatted_sentences = ["".join(sentences[i:i+2]) for i in range(0, len(sentences), 2)]
        return formatted_sentences


    def generate_sentence_timestamps(self, script, video_duration):
        sentences = self.script_to_list(script)
        total_words = len(script.split())
        avg_word_duration = video_duration / total_words
        sentence_timestamps = []
        current_time = 0.0
        for sentence in sentences:
            num_words_in_sentence = len(sentence.split())
            sentence_duration = num_words_in_sentence * avg_word_duration
            sentence_timestamps.append((sentence, current_time, current_time + sentence_duration))
            current_time += sentence_duration
        return sentence_timestamps
    
    def generate_and_download_images(self, sentence_list, num_images=3):
        if os.path.exists(f'{self.folder_name}/images'):
            print(f'images exist at {self.folder_name}/images')
            return
        for i in range(num_images):
            if sentence_list:
                prompt = sentence_list.pop(0)
                midjourney_api = MidjourneyApi(prompt, f"{self.folder_name}/images/image{i}.png")
                midjourney_api.download_image()
            else:
                break

    def getVideo(self, target_length, query):
        path = f'{self.folder_name}/video.mp4'
        print(query)
        if self.metadata_manager.check_metadata(Constants.video, self.folder_name):
            return VideoFileClip(path)
        data = self.get_video_data(query)
        clips, temp_files = self.generate_clips(data, target_length, query)
        final_clip = concatenate_videoclips(clips)
        final_clip.write_videofile(path, codec='libx264')
        for clip in clips:
            clip.close()
        
        return final_clip

    def get_video_data(self, query):
        url = f'https://pixabay.com/api/videos/?key={os.getenv("PIXABAY_KEY")}&q={query}'
        response = requests.get(url)
        data = {}
        if response.status_code == 200:
            data = response.json() 
        else:
            print(f"Request failed with status code {response.status_code}")
        return data

    def generate_clips(self, data, target_length, query):
        clips = []
        temp_files = []
        videos = data["hits"]
        current_length = 0
        num_videos = len(videos)  # Get the total number of videos

        # Create a list of video indices, then shuffle it
        indices = list(range(num_videos))
        random.shuffle(indices)

        for idx in indices:  # Iterate over shuffled indices
            if current_length >= target_length:
                break
            temp_video_path = f'{query}{idx}.mp4'
            Utils.download_file(videos[idx]["videos"]["medium"]["url"], temp_video_path)
            clip, segment_length = self.get_clip_segment(temp_video_path, target_length, current_length)
            clips.append(clip)
            current_length += segment_length
            temp_files.append(temp_video_path)  # Save temp file path

        return clips, temp_files


    def get_clip_segment(self, temp_video_path, target_length, current_length):
        full_clip = VideoFileClip(temp_video_path)
        video_length = full_clip.duration
        max_length = min(7, video_length) 
        min_length = min(5, max_length) 
        segment_length = random.uniform(min_length, max_length) 
        segment_length = min(segment_length, target_length - current_length)
        start_time = random.uniform(0, video_length - segment_length)  
        end_time = start_time + segment_length
        clip = full_clip.subclip(start_time, end_time)
        clip = clip.resize(height=1920)  # Resize the height first
        w, h = clip.size
        clip = clip.crop(x_center=w/2, y_center=h/2, width=9*h/16, height=h)  # Crop to 9:16 ratio
        return clip, segment_length


    def build_prompt(self, user_input):
        intro = f"Generate a short, motivational script that offers a positive and encouraging message related to the theme: '{user_input}'.\n\n"
        script_prompt = f"{intro}The script should be short (10 seconds). The script should provide an uplifting perspective on common human experiences or feelings, similar to these examples: \n\n 1. 'Struggling to love yourself? Remember, the most powerful relationship you'll ever have is the relationship with yourself. Cherish and nurture it.' \n\n 2. 'Feeling overwhelmed with negativity? Let's turn it around. Find one thing to be grateful for each day, and watch how your perspective changes.' \n\n Please continue in a similar style."
        
        return script_prompt

    def get_random_music_file(self, folder="music"):
        music_files = os.listdir(folder)  # Lists all files in the directory
        music_files = [f for f in music_files if f.endswith(".mp3")]  # Filter out non-music files
        if not music_files:
            raise Exception("No music files found in directory")
        return os.path.join(folder, random.choice(music_files))  # Picks a random file and returns the path
    
    def build_thumbnail_prompt(self, audio_prompt):
        purpose = "informative"
        keywords = ["how to", "why", "guide", "tutorial", "strategy", "tips", "methods"]
        prompt = f'Create a catchy and SEO-friendly thumbnail text for a {purpose} YouTube video titled "{audio_prompt}". The text should be short (5 words or less) and could include some of the following keywords: {", ".join(keywords)}.'
        return prompt
    
    def build_title_prompt(self, script):
        prompt = f'Generate a catchy and inspiring title for a YouTube Shorts video. Keep it short (5 words). The video offers a motivational message about self-improvement and personal growth. The script is {script}'
        return prompt
    
    def build_description_prompt(self, script):
        prompt = f'Compose a captivating and detailed description for a YouTube Shorts video. Keep it short (15 words). The video is a minute-long motivational clip focusing on the themes of self-love and personal development. The script is {script}'
        return prompt

    def saveText(self, prompt, resource_type):
        script_path = os.path.join(self.folder_name, f'{resource_type}.txt')
        if self.metadata_manager.check_metadata(resource_type, self.folder_name):
            with open(script_path, 'r') as f:
                text = f.read()
            return text
        text = self.generate_text(prompt)
        os.makedirs(self.folder_name, exist_ok=True)
        with open(os.path.join(self.folder_name, f'{resource_type}.txt'), 'w') as f:
            f.write(text)
        return text

    def generate_thumbnail(self, video_type, audio_prompt):
        logging.info("Creating thumbnail...")
        thumbnail_prompt = self.build_thumbnail_prompt(audio_prompt)
        thumbnail_text = self.saveText(thumbnail_prompt, Constants.thumbnail).replace('"', '')
        Image_Manager.create_thumbnail_with_text(video_type, thumbnail_text, f'{self.folder_name}')

    def generate_script_and_audio(self, audio_prompt):
        logging.info(f"Generating script for {audio_prompt}...")
        prompt = self.build_prompt(audio_prompt)
        script = self.saveText(prompt, Constants.script)
        logging.info("Generating audio...")
        audio_path = self.audio_generator.getBadAudio(script, self.folder_name)
        return script, audio_path

    def get_music(self, duration):
        music_path = self.get_random_music_file()
        music = AudioFileClip(music_path).volumex(0.1)
        latest_start_time = max(0, music.duration - duration)
        start_time = random.uniform(0, latest_start_time)
        music_clip = music.subclip(start_time, start_time + duration)
        return music_clip

    def makeVideo(self):
        backgrounds = [
            'water', 
            'forest', 
            'mountains', 
            'desert', 
            'stars',
            'sunrise',
            'sunset',
            'beach',
            'cityscape',
            'river',
            'snow',
            'rain',
            'clouds',
            'moon',
            'ocean',
            'lake',
            'tundra',
            'jungle',
            'night sky',
            'volcano'
        ]
        themes = [
            'self-love', 
            'gratitude', 
            'perseverance', 
            'decision-making', 
            'self-worth', 
            'new beginnings',
            'embracing change',
            'mindfulness',
            'overcoming fear',
            'resilience',
            'personal growth',
            'positivity',
            'forgiveness',
            'patience',
            'empathy',
            'compassion',
            'creativity',
            'courage',
            'kindness',
            'optimism',
            'passion',
            'mind-body connection',
            'joy',
            'peace',
            'spirituality',
            'balance',
            'inner strength',
            'harmony'
        ]
        background = random.choice(backgrounds)
        audio_prompt = random.choice(themes)
        script = None
        if script is None:
            logging.info(f"Generating script for {audio_prompt}...")
            prompt = self.build_prompt(audio_prompt)
            script = self.saveText(prompt, Constants.script)
        else:
            logging.info(f"Using provided script for {audio_prompt}...")
        audio_clip = self.audio_generator.getBadAudio(script, self.folder_name)
        video_clip = self.getVideo(audio_clip.duration, background)
        music_clip = self.get_music(video_clip.duration)
        sentences = self.script_to_list(script)
        #self.generate_and_download_images(sentences, video.get('images'))
        video_duration = video_clip.duration
        durations = self.generate_sentence_timestamps(script, video_duration)
        clips = self.story_manager.get_random_clips(sentences, f'{self.folder_name}/images', durations)
        
        video_clip = video_clip.set_audio(CompositeAudioClip([audio_clip, music_clip]))
        final_video = self.story_manager.add_clips_to_video([video_clip], clips)
        metadata_title = self.generate_text(self.build_title_prompt(script)).strip('"')
        metadata_desc = self.generate_text(self.build_description_prompt(script)).strip('"')
        print(metadata_title)
        print(metadata_desc)
        video_metadata = {
            "snippet": {
                "title": f'{metadata_title} #shorts' ,
                "description": f'{metadata_desc}' ,
                "tags": [],
                "categoryId": "22"  # Category ID for People & Blogs; can be changed according to your need
            },
            "status": {
                "privacyStatus": "public",  # or "public" or "unlisted"
                "selfDeclaredMadeForKids": False,
            }
        }
        
        if not os.path.exists(f'{self.folder_name}/videoFinal.mp4'):
            final_video.write_videofile(f'{self.folder_name}/videoFinal.mp4', codec='libx264')
        final_video.close()
        #upload_video(f'{self.folder_name}/videoFinal.mp4', video_metadata)
        logging.info("Video creation complete!")
    




def makeVideo():
    # Set up logging
    logging.basicConfig(level=logging.INFO)
    video_data = Utils.load_json("common/video/video_input.json")
    current_date = datetime.now()

    # Convert to string
    datetime_string = current_date.strftime("%Y-%m-%d_%H-%M-%S")
    for category, category_data in video_data.items():
        for i in range(0,1):
            vg = VideoGenerator(f'{Constants.video_file_path}{Utils.sanitize_folder_name(datetime_string)}{i}')
            vg.makeVideo()
    Utils.remove_mp4_files('')

