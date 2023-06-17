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

        # draw outline
        draw.text((0, 0), text, fill=outline_color, font=font, stroke_width=2, stroke_fill=outline_color)
        # draw text
        draw.text((0, 0), text, fill=text_color, font=font)

        return image

    def add_text_with_outline(self, text, fontsize, color):
    # Create a new image with alpha channel (RGBA)
        img = Image.new('RGBA', (1, 1))

        # Create a draw object
        draw = ImageDraw.Draw(img)

        # Get the size of the text
        font = Image_Manager.getFont(fontsize)
        text_size = draw.textsize(text, font=font)

        # Create a new image with enough size for the text and the outline
        img = Image.new('RGBA', (text_size[0] + 4, text_size[1] + 4))

        # Update the draw object
        draw = ImageDraw.Draw(img)

        # Draw a semi-transparent rectangle behind the text
        draw.rectangle(((0, 0), (text_size[0] + 4, text_size[1] + 4)), fill=(0, 0, 0, 128))

        # Draw outline
        outline_range = range(3)
        for x in outline_range:
            for y in outline_range:
                draw.text((x - 1, y - 1), text, font=font, fill="black")

        # Draw the text
        draw.text((1, 1), text, font=font, fill=color)

        # Convert the image into numpy array and create a clip
        np_img = np.array(img)
        return np_img

    def addSpeedReadingToVideo(self, video_path, word_timestamps):
    # Load video
        video = VideoFileClip(video_path)
        print(word_timestamps)
        # Generate text clips for each word group
        text_clips = []
        for word_group, start_time, end_time in word_timestamps:
            text_clip_img = self.add_text_with_outline(word_group, fontsize=150, color='white')
            text_clip = ImageClip(np.array(text_clip_img), duration=(end_time - start_time)).set_start(start_time).set_position('center')
            text_clips.append(text_clip)

        # Overlay the text clips on the video
        video_with_text = CompositeVideoClip([video] + text_clips)

        # Write the final video to a file
        final_path = video_path.replace(".mp4", "Final.mp4")
        video_with_text.write_videofile(final_path, codec='libx264')

        return final_path




    def getSlideInAndFadeOutImageClip(self, image_file, start_time, duration, video_size):
        fade_duration = 2
        half_duration = (duration - fade_duration) / 2
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

    def addImageToVideo(self, video_path, images_folder, sentences):
        original = video_path[0:-4]
        final_location = original + "Final" + ".mp4"

        if self.metadata_manager.check_metadata(Constants.final_video, f'{Constants.video_file_path}{self.folder_name}'):
            return final_location
        video = VideoFileClip(video_path)
        image_files = self.getSortedImageFiles(images_folder)

        clips = [video]
        duration = 0
        for i, image_file in enumerate(image_files):
            start_time = 1 + (i * duration)
            text_clip = (TextClip(sentences[i], fontsize=70, color='white')
                .set_position('bottom')
                .set_duration(duration)
                .set_start(start_time))
            
            duration += 7
            if start_time + duration > video.duration - 2:
                break

            image_clip = self.getSlideInAndFadeOutImageClip(image_file, start_time, duration, video.size)
            clips.append(image_clip)
            clips.append(text_clip)

        
        final_clip = CompositeVideoClip(clips)

        final_clip.write_videofile(f'{final_location}', codec='libx264')

        return final_location
