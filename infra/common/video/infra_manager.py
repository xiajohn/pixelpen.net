# longvideogenerator.py

from moviepy.editor import concatenate_videoclips, VideoFileClip
import pixabay
import os
import requests
from dotenv import find_dotenv, load_dotenv
from common.utils import download_file
load_dotenv(find_dotenv('../../.env'))
class LongVideoGenerator:
    def __init__(self):
        self.px = pixabay.core(os.getenv("PIXABAY_KEY"))

    def get_long_video(self, length, query):
        # Search for videos

        url = f'https://pixabay.com/api/videos/?key={os.getenv("PIXABAY_KEY")}&q=yellow+flowers&pretty=true'
        response = requests.get(url)
        data = {}
        # If the request was successful, response.status_code will be 200
        if response.status_code == 200:
            data = response.json()  # parse the response as JSON
        else:
            print(f"Request failed with status code {response.status_code}")


        # Create an empty array to hold our video clips
        clips = []

        print(f'length:{len(data)}')

        # Download each video and create a VideoFileClip object
        # Continue downloading clips until we reach the desired length
        videos = data["hits"]
        i = 0
        while i < length:
            download_file(videos[i]["videos"]["medium"]["url"], f'{query}{i}.mp4')

            clip = VideoFileClip(f'{query}{i}.mp4')
            clips.append(clip)
            i += 1

        # Concatenate the video clips together
        final_clip = concatenate_videoclips(clips)

        # Write the video without audio to a file
        final_clip.write_videofile(f'generated/video/{query}_long_video.mp4', codec='libx264')

        # Delete the downloaded videos
        # for i in range(len(clips)):
        #     os.remove(f'{query}{i}.mp4')

        # Return the path to the final video clip
        return f'{query}_long_video.mp4'
def makeLongVideo():
    lvg = LongVideoGenerator()
    long_video_path = lvg.get_long_video(10, "space")