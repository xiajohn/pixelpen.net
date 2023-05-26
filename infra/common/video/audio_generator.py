import os
import requests
import json
from common.content_generator import ContentGenerator
from common.utils import download_file
class AudioGenerator(ContentGenerator):
    def __init__(self):
        pass

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
        return download_file(self.parse_sse_events(response.text), "generated/audio/test.mp3")


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
