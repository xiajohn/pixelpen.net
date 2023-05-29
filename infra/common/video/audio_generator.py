import os
import time
import requests
import json
import logging
from common.content_generator import ContentGenerator
from utils import Utils
from moviepy.editor import concatenate_videoclips, VideoFileClip, AudioFileClip, ImageClip, CompositeVideoClip, CompositeAudioClip
from common.video.constants import Constants
class AudioGenerator(ContentGenerator):
    def __init__(self):
        pass

    def getAudio(self, text, folder_name, voice="larry", filename="audio"):
        audio_path = f'{Constants.video_file_path}{folder_name}{filename}.mp3'
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
        print(response)
        Utils.download_file(self.parse_sse_events(response.text), audio_path)
        return audio_path
    
    def addAudio(self, video_path, audio_path, music_path, query):
        folder_name = Utils.sanitize_folder_name(query)
        if self.metadata_manager.check_metadata(Constants.audio, folder_name):
            logging.info("video exists")
            return
        # Load the video
        final_clip = VideoFileClip(video_path)

        # Load the audio files
        audio = AudioFileClip(audio_path)
        music = AudioFileClip(music_path)

        # Make sure the music track is not louder than the audio track
        music = music.volumex(0.1)
        audio = audio.volumex(0.6)
        # If the music is longer than the main audio, cut it
        if music.duration > audio.duration:
            music = music.subclip(0, audio.duration)
        print("music duration")
        print(music.duration)
        final_clip = VideoFileClip(video_path).set_duration(music.duration + 5)

        # Combine the audio tracks
        final_audio = CompositeAudioClip([audio, music])

        # Set the final audio track to the video
        final_clip = final_clip.set_audio(final_audio)

        # Write the final video file
        final_clip.write_videofile(f'{video_path}', codec='libx264')
       # self.metadata_manager.update_metadata(folder_name, Constants.audio)
        return video_path
    
    def getBadAudio(self, text, folder_name, voice="en-US-JennyNeural", filename="audio.mp3"):
        audio_path = f'{folder_name}/{filename}'
        if self.metadata_manager.check_metadata(Constants.audio, folder_name):
            logging.info("audio exists")
            return audio_path
        
        url = "https://play.ht/api/v1/convert"
        payload = {
            "content": [text],
            "voice": voice
        }
        headers = {
            "accept": "text/event-stream",
            "content-type": "application/json",
            "AUTHORIZATION": f'Bearer {os.getenv("TEXT_TO_SPEECH_API_KEY")}',
            "X-USER-ID": "6cSsgiLC0zOxKZ5qTjlauADGYju2"
        }

        response = requests.post(url, json=payload, headers=headers)
        id = self.parse_bad_audio_sse_events(response.text)["transcriptionId"]
        print(id)
        Utils.download_file(
            self.getBadAudioURL(id),
            audio_path
        )
        return audio_path

    def getBadAudioURL(self, id):
        time.sleep(2)
        url = f'https://play.ht/api/v1/articleStatus?transcriptionId={id}'
        headers = {
            "accept": "application/json",
            "AUTHORIZATION": f'Bearer {os.getenv("TEXT_TO_SPEECH_API_KEY")}',
            "X-USER-ID": "6cSsgiLC0zOxKZ5qTjlauADGYju2"
        }

        response = requests.get(url, headers=headers)
        
        return self.parse_bad_audio_sse_events(response.text)['audioUrl']

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

    def parse_bad_audio_sse_events(self, text):
        events = text.strip().split("\n\n")
        for event in events:
            lines = event.split("\n")
            for line in lines:
                print(line)
                return json.loads(line)

