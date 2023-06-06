from moviepy.editor import concatenate_videoclips, VideoFileClip, AudioFileClip, ImageClip, CompositeVideoClip, CompositeAudioClip
from common.metadata_manager import MetadataManager
from moviepy.video.fx.all import fadein
import os
from common.constants import Constants
class StoryManager:
    def __init__(self, folder_name):
        self.folder_name = folder_name
        self.metadata_manager = MetadataManager()

    

    def addImageToVideo(self, video_path, images_folder):
        original = video_path[0:-4]
        final_location = original + "Final" + ".mp4"

        if self.metadata_manager.check_metadata(Constants.final_video, f'{Constants.video_file_path}{self.folder_name}'):
            return final_location
        video = VideoFileClip(video_path)

        # Get a sorted list of all image file paths in the directory
        image_files = sorted([os.path.join(images_folder, f) for f in os.listdir(images_folder) if f.endswith(('.png'))])

        clips = [video]  # Start with the video as the first clip

        for i, image_file in enumerate(image_files):
            start_time = 1 + i * 5
            duration = 5  # Each image lasts 5 seconds
            if start_time + duration > video.duration - 2:  # Stop adding images 2 seconds before the video ends
                break

            image = (ImageClip(image_file)
                    .set_duration(duration)
                    .set_start(start_time)
                  #  .resize(620)
                    .set_position(('center', 'center')))
            clips.append(image)

        final_clip = CompositeVideoClip(clips)

        final_clip.write_videofile(f'{final_location}', codec='libx264')

        return f'{final_location}'