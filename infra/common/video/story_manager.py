from moviepy.editor import concatenate_videoclips, VideoFileClip, AudioFileClip, ImageClip, CompositeVideoClip, TextClip
from common.metadata_manager import MetadataManager
from moviepy.video.fx.all import fadein, fadeout
from clients.midjourney_api import MidjourneyApi
import os
from common.constants import Constants

class StoryManager:
    def __init__(self, folder_name):
        self.folder_name = folder_name
        self.metadata_manager = MetadataManager()

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
