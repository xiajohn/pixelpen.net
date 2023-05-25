from moviepy.editor import concatenate_videoclips, VideoFileClip, AudioFileClip
import pixabay
import os
import requests

from common.content_generator import ContentGenerator
import json
from dotenv import find_dotenv, load_dotenv
load_dotenv(find_dotenv('../../.env'))
class VideoGenerator(ContentGenerator):
    def __init__(self):
        self.px = pixabay.core("36698641-c842e81e37a10423a32c4ad34")

    def getVideo(self, length, query):
        # Search for videos
        videos = self.px.queryVideo(query)

        if len(videos) == 0:
            raise Exception("No videos found")

        # Create an empty array to hold our video clips
        clips = []
        print("{} hits".format(len(videos)))
        # Download each video and create a VideoFileClip object
        for i in range(3):
            videos[i].download(f'space{i}.mp4', "large")
            clips.append(VideoFileClip(f'space{i}.mp4'))

        # Concatenate the video clips together
        final_clip = concatenate_videoclips(clips)

        # If the final clip is shorter than the desired length, loop it
        # if final_clip.duration < length:
        #     final_clip = final_clip.loop(duration=length)

        # # If the final clip is longer than the desired length, cut it
        # if final_clip.duration > length:
        #     final_clip = final_clip.subclip(0, length)

        # Write the video without audio to a file
        final_clip.write_videofile(f'{query}_without_audio.mp4', codec='libx264')

        # Delete the downloaded videos
        # for i in range(3):
        #     os.remove(f'space{i}.mp4')

        # Return the path to the final video clip
        return f'{query}_without_audio.mp4'
    
    def getAudio(self, text, voice="larry", filename="audio.mp3"):
        url = "https://play.ht/api/v2/tts"
        payload = {
            "quality": "high",
            "output_format": "mp3",
            "speed": 1,
            "sample_rate": 24000,
            "text": text,
            "voice": voice
        }
        headers = {
            "accept": "text/event-stream",
            "content-type": "application/json",
            "AUTHORIZATION": f'Bearer {os.getenv("TEXT_TO_SPEECH_API_KEY")}',
            "X-USER-ID": "6cSsgiLC0zOxKZ5qTjlauADGYju2"
        }

        response = requests.post(url, json=payload, headers=headers)
        return self.download_file(self.parse_sse_events(response.text), "test.mp3")


    def parse_sse_events(self, text):
        events = text.strip().split("\n\n")
        for event in events:
            lines = event.split("\n")
            for line in lines:
                if line.startswith("data:"):
                    data = line[5:]
                    try:
                        payload = json.loads(data)
                    except json.JSONDecodeError:
                        continue
                    if payload.get("stage") == "complete":
                        return payload.get("url")
        return None


    def download_file(self, url, filename):
        response = requests.get(url)
        with open(filename, 'wb') as f:
            f.write(response.content)
        return filename

    def addAudio(self, video_path, audio_path):
        # Load the video
        final_clip = VideoFileClip(video_path)

        # Add the audio to the video
        audio = AudioFileClip(audio_path)
        final_clip = final_clip.set_audio(audio)

        # Write the result to a file
        final_clip.write_videofile(f'{video_path[:-4]}_with_audio.mp4', codec='libx264')

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
