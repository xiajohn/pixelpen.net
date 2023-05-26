from moviepy.editor import concatenate_videoclips, VideoFileClip, AudioFileClip, ImageClip, CompositeVideoClip
import pixabay
import os
import requests
from moviepy.video.fx.all import fadeout
from moviepy.video.compositing.transitions import slide_in, slide_out

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
    
    def addImage(self, video_path, image_path, start_time, end_time):
    # Load the video
        video = VideoFileClip(video_path)
            
        # Load the image
        image = ImageClip(image_path)

        # Resize and center the image
        image = image.resize(width=620)  # Resize width keeping aspect ratio

        # Define the time when image should start sliding out
        slide_out_start_time = end_time - start_time - 2  # 2 seconds before the end_time

        # Set image position to be centered initially, then slide out and fade after slide_out_start_time
        image = image.set_position(('center', 'center')).set_start(start_time).set_duration(end_time - start_time)
        
        # Add the image to the video
        final_clip = CompositeVideoClip([video, image.set_duration(video.duration)])

        # Write the result to a file
        final_clip.write_videofile(f'{video_path[:-4]}_with_image.mp4', codec='libx264')

        return f'{video_path[:-4]}_with_image.mp4'


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
    # prompt = vg.build_prompt("meditation")
    # script = vg.generate_text(prompt)
    # audio_path = vg.getAudio(script)
    # video_path = vg.getVideo(30, "space")
    # vg.addAudio(video_path, audio_path)

    image_path = 'generated/alki-beach/image_data_1.jpg'  # replace with your image path
    start_time = 1  # replace with when you want the image to appear
    end_time = 10  # replace with when you want the image to disappear
    video_with_image_path = vg.addImage("generated/space_without_audio_with_audio.mp4", image_path, start_time, end_time)
