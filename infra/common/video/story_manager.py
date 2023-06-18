from moviepy.editor import concatenate_videoclips, VideoFileClip, AudioFileClip, ImageClip, CompositeVideoClip, TextClip, ImageSequenceClip
from common.metadata_manager import MetadataManager
from moviepy.video.fx.all import fadein, fadeout
from clients.midjourney_api import MidjourneyApi
import os
import numpy as np
from common.constants import Constants
from PIL import Image, ImageDraw, ImageFont
from common.makememe.generator.design.image_manager import Image_Manager
class StoryManager:
    def __init__(self, folder_name):
        self.folder_name = folder_name
        self.metadata_manager = MetadataManager()

    def create_text_image(self, text, font_size, outline_color, text_color):
        font = ImageFont.truetype("arial", font_size)
        text_width, text_height = font.getsize(text)
        image = Image.new('RGBA', (text_width, text_height), (0, 0, 0, 0))
        draw = ImageDraw.Draw(image)
        draw.text((0, 0), text, fill=outline_color, font=font, stroke_width=2, stroke_fill=outline_color)
        draw.text((0, 0), text, fill=text_color, font=font)
        return image

    def add_text_with_outline(self, text, fontsize, color):
        img = Image.new('RGBA', (1, 1))
        draw = ImageDraw.Draw(img)
        font = Image_Manager.getFont(fontsize)
        text_size = draw.textsize(text, font=font)
        img = Image.new('RGBA', (text_size[0] + 4, text_size[1] + 5))
        draw = ImageDraw.Draw(img)
        draw.rectangle(((0, 0), (text_size[0] + 4, text_size[1] + 5)), fill=(0, 0, 0, 128))
        outline_range = range(3)
        for x in outline_range:
            for y in outline_range:
                draw.text((x - 1, y - 1), text, font=font, fill="black")
        draw.text((1, 1), text, font=font, fill=color)
        np_img = np.array(img)
        return np_img

    def getTextClip(self, text, start_time, end_time):
        wrapped_text = self.wrap_text(text, 5)  # wrap text if more than 5 words
        text_clip_img = self.add_text_with_outline(wrapped_text, fontsize=150, color='white')
        text_clip = ImageClip(np.array(text_clip_img), duration=(end_time - start_time)).set_start(start_time).set_position('center')

        return text_clip


    def getSlideInAndFadeOutImageClip(self, image_file, start_time, duration, video_size):
        fade_duration = 2
        image = (ImageClip(image_file)
                .resize(height=int(video_size[1] * 0.7))  
                .set_duration(duration)
                .set_start(start_time)
                .fadein(1)
                .fadeout(fade_duration)  
                .set_position('center')
                )
        return image

    def getSortedImageFiles(self, images_folder):
        return sorted([os.path.join(images_folder, f) for f in os.listdir(images_folder) if f.endswith(('.png', '.jpg'))])
    
    def wrap_text(self, text, limit):
        words = text.split()
        if len(words) <= limit:
            return text
        else:
            lines = [' '.join(words[i:i+limit]) for i in range(0, len(words), limit)]
            return '\n'.join(lines)


    def get_random_clips(self, sentences, images_folder, durations):
        image_files = self.getSortedImageFiles(images_folder)
        num_images = len(image_files)
        num_nothings = 2
        clip_types = ['sentence'] * len(sentences) + ['image'] * num_images + ['nothing'] * num_nothings
        np.random.shuffle(clip_types)
        clips = []
        for sentence, duration, clip_type in zip(sentences, durations, clip_types):
            _, start_time, end_time = duration
            clip_info = {
                "type": clip_type,
                "content": sentence if clip_type == 'sentence' else (image_files.pop() if clip_type == 'image' else ''),
                "start_time": start_time,
                "end_time": end_time
            }
            clips.append(clip_info)

        return clips

    def add_clips_to_video(self, video_path, clips):
        original_video = VideoFileClip(video_path)
        final_clips = [original_video]

        # Keep track of the cumulative duration of added clips
        cumulative_duration = 0

        for clip in clips:
            if clip['type'] == 'sentence':
                clip_duration = clip['end_time'] - clip['start_time']
                # Check if adding this clip would exceed the original video duration
                if cumulative_duration + clip_duration > original_video.duration:
                    break
                text_clip = self.getTextClip(clip['content'], clip['start_time'], clip['end_time'])
                final_clips.append(text_clip)
                cumulative_duration += clip_duration

            elif clip['type'] == 'image':
                start_time, end_time = clip['start_time'], clip['end_time']
                clip_duration = end_time - start_time
                # Check if adding this clip would exceed the original video duration
                if cumulative_duration + clip_duration > original_video.duration:
                    break
                image_clip = self.getSlideInAndFadeOutImageClip(clip['content'], start_time, end_time, original_video.size)
                final_clips.append(image_clip)
                cumulative_duration += clip_duration

            elif clip['type'] == 'nothing':
                continue

        final_video = CompositeVideoClip(final_clips)

        final_path = video_path.replace(".mp4", "Final.mp4")
        final_video.write_videofile(final_path, codec='libx264')

        return final_path



