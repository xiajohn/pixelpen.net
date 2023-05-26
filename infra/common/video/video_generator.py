from moviepy.editor import concatenate_videoclips, VideoFileClip, AudioFileClip
import pixabay
import os
import requests
from common.video.audio_generator import AudioGenerator
from common.utils import download_file
import json
from dotenv import find_dotenv, load_dotenv
load_dotenv(find_dotenv('../../.env'))
class VideoGenerator(AudioGenerator):
    def __init__(self):
        self.px = pixabay.core(os.getenv("PIXABAY_KEY"))

    def getVideo(self, length, query):
        # Search for videos
        videos = self.px.queryVideo(query)

        if len(videos) == 0:
            raise Exception("No videos found")

        # Create an empty array to hold our video clips
        clips = []
        print("{} hits".format(len(videos)))
        for i in range(3):
            videos[i].download(f'space{i}.mp4', "large")
            clips.append(VideoFileClip(f'space{i}.mp4'))

        final_clip = concatenate_videoclips(clips)
        final_clip.write_videofile(f'{query}_without_audio.mp4', codec='libx264')

        # Delete the downloaded videos
        # for i in range(3):
        #     os.remove(f'space{i}.mp4')

        # Return the path to the final video clip
        return f'{query}_without_audio.mp4'

    def addAudio(self, video_path, audio_path):
        # Load the video
        final_clip = VideoFileClip(video_path)

        # Add the audio to the video
        audio = AudioFileClip(audio_path)
        final_clip = final_clip.set_audio(audio)

        # Write the result to a file
        final_clip.write_videofile(f'generated/video/{video_path[:-4]}_with_audio.mp4', codec='libx264')

    def build_prompt(self, user_input):
        # Start the prompt with a few sentences introducing the video.
        intro = f"In this video, we're going to talk about {user_input}.\n\n"
        
        # Ask GPT-4 to continue the script in a friendly and informative style.
        script_prompt = f"{intro} {user_input} is a fascinating topic, and there's so much to cover. Can you provide a friendly and informative script for a 1-minute video on this topic? Start the response with the script immediately. Do not include new line characters."
        
        return script_prompt

def makeVideo():
    vg = VideoGenerator()
    prompt = vg.build_prompt("meditation")
    script = vg.generate_text(prompt)
    audio_path = vg.getAudio(script)
    video_path = vg.getVideo(30, "space")
    vg.addAudio(video_path, audio_path)
