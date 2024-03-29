import os
import time
import requests
import json
import logging
from common.metadata_manager import MetadataManager
from common.content_generator import ContentGenerator
from utils import Utils
from moviepy.editor import concatenate_videoclips, VideoFileClip, AudioFileClip, ImageClip, CompositeVideoClip, CompositeAudioClip, afx
from common.constants import Constants
class AudioGenerator(ContentGenerator):
    def __init__(self):
        self.metadata_manager = MetadataManager()

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
    
    def addAudio(self, video_path, audio_path, music_path, folder_name):
        original = video_path[0:-4]
        final_location = original + "Audio" + ".mp4"
        if self.metadata_manager.check_metadata(Constants.video_with_audio, folder_name):
            return AudioFileClip(final_location)
        audio = AudioFileClip(audio_path).fx(afx.volumex, 0.7)
        music = AudioFileClip(music_path).fx(afx.volumex, 0.3)
        if music.duration > audio.duration:
            music = music.subclip(0, audio.duration)
        final_clip = VideoFileClip(video_path).subclip(0, audio.duration)
        final_audio = CompositeAudioClip([audio, music])
        final_clip = final_clip.set_audio(final_audio)
        final_clip.write_videofile(f'{final_location}', codec='libx264')
        return final_location
    
    def getBadAudio(self, text, folder_name, voice="en-US-JennyNeural", filename="audio.mp3"):
        audio_path = f'{folder_name}/{filename}'
        if self.metadata_manager.check_metadata(Constants.audio, folder_name):
            return AudioFileClip(audio_path)
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
        return AudioFileClip(audio_path)

    def getBadAudioURL(self, id):
        time.sleep(5)
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

