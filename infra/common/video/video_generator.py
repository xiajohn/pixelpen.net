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
class VideoGenerator(AudioGenerator):
    def __init__(self):
        self.px = pixabay.core(os.getenv("PIXABAY_KEY"))

    def getVideo(self, length, query):
        videos = self.px.queryVideo(query)
        path = f'{Constants.video_file_path}{query}.mp4'
        if len(videos) == 0:
            raise Exception("No videos found")
        clips = []
        print("{} hits".format(len(videos)))
        for i in range(3):
            videos[i].download(f'space{i}.mp4', "large")
            clips.append(VideoFileClip(f'space{i}.mp4'))

        final_clip = concatenate_videoclips(clips)
        final_clip.write_videofile(path, codec='libx264')

        # Delete the downloaded videos
        # for i in range(3):
        #     os.remove(f'space{i}.mp4')

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

    def addAudio(self, video_path, audio_path, music_path):
        # Load the video
        final_clip = VideoFileClip(video_path)

        # Load the audio files
        audio = AudioFileClip(audio_path)
        music = AudioFileClip(music_path)

        # Make sure the music track is not louder than the audio track
        music = music.volumex(0.1)

        # If the music is longer than the main audio, cut it
        if music.duration > audio.duration:
            music = music.subclip(0, audio.duration)



        # Combine the audio tracks
        final_audio = CompositeAudioClip([audio, music])

        # Set the final audio track to the video
        final_clip = final_clip.set_audio(final_audio)

        # Write the final video file
        final_clip.write_videofile(f'{video_path}', codec='libx264')

        return video_path

    def build_prompt(self, user_input):
        intro = f"In this video, we're going to dive right into the exciting world of {user_input}.\n\n"
        script_prompt = f"{intro}We want to start the video with a captivating hook. For instance, you could start with something like 'Imagine a world where {user_input} is at the forefront of every conversation.' But remember, that's just an example. We want you to come up with an original and engaging hook that fits the topic of {user_input}. After the hook, proceed directly into the informative content."
        return script_prompt

    
    def downloadMusic(self, query):
        music_files = self.px.queryAudio(query)

        if len(music_files) == 0:
            raise Exception("No music files found")
        
        print("{} hits".format(len(music_files)))
        
        # Download the first music file
        music_files[0].download(f'{query}_music.mp3', "large")
        
        # Return the path to the music file
        return f'{query}_music.mp3'

def makeVideo():
    # Set up logging
    logging.basicConfig(level=logging.INFO)
    vg = VideoGenerator()

    logging.info("Generating script...")
    prompt = vg.build_prompt("first year of artificial intelligence")
    script = vg.generate_text(prompt)
    audio_path = vg.getAudio(script)
    music_path = f'{Constants.audio_file_path}relaxed-vlog-night-street-131746.mp3'
    logging.info("Generating video...")
    video_path = vg.getVideo(30, "psychedelic")
    
    logging.info("Adding audio to video...")
    vg.addAudio(video_path, audio_path, music_path)

    logging.info("Downloading music...")
   # music_path = vg.downloadMusic("relaxing")

    image_path = 'generated/alki-beach/image_data_1.jpg'  # replace with your image path
    start_time = 1  # replace with when you want the image to appear
    duration = 13

    logging.info("Adding image to video...")
    vg.addImage(video_path, image_path, start_time, duration)

    logging.info("Video creation complete!")