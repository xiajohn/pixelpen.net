from moviepy.editor import concatenate_videoclips, VideoFileClip, AudioFileClip, ImageClip, CompositeVideoClip, CompositeAudioClip
from common.metadata_manager import MetadataManager
from moviepy.video.fx.all import fadein, fadeout
import os
from common.constants import Constants

class StoryManager:
    def __init__(self, folder_name):
        self.folder_name = folder_name
        self.metadata_manager = MetadataManager()

    def getSlideInAndFadeOutImageClip(self, image_file, start_time, duration, video_size):
        """Returns an ImageClip with slide-in and fade-in effects applied."""
        fade_duration = 2
        half_duration = (duration - fade_duration) / 2
        image = (ImageClip(image_file)
                 .resize(height=int(video_size[1] * 0.8))  # Resize image to 80% of the height of the video before adding it to the clip
                 .set_duration(duration)  # Slide-in phase lasts for half of the duration
                 .set_start(start_time)
                 .fadein(1)  # Apply the fade-in effect over 1 second
                 .fadeout(fade_duration)  # Apply the fade-out effect over 2 seconds
                 .set_position(lambda t: (min(t/half_duration * video_size[0]/2, video_size[0]/2), 'center'))  # Slide in then stop
                 )
        return image

    def getSortedImageFiles(self, images_folder):
        """Returns a sorted list of image file paths from the given folder."""
        return sorted([os.path.join(images_folder, f) for f in os.listdir(images_folder) if f.endswith(('.png', '.jpg'))])

    def addImageToVideo(self, video_path, images_folder):
        original = video_path[0:-4]
        final_location = original + "Final" + ".mp4"

        if self.metadata_manager.check_metadata(Constants.final_video, f'{Constants.video_file_path}{self.folder_name}'):
            return final_location
        video = VideoFileClip(video_path)

        image_files = self.getSortedImageFiles(images_folder)

        clips = [video]  # Start with the video as the first clip

        for i, image_file in enumerate(image_files):
            start_time = 1 + i * 5
            duration = 5  # Each image lasts 5 seconds
            if start_time + duration > video.duration - 2:  # Stop adding images 2 seconds before the video ends
                break

            image_clip = self.getSlideInAndFadeOutImageClip(image_file, start_time, duration, video.size)
            clips.append(image_clip)

        final_clip = CompositeVideoClip(clips)

        final_clip.write_videofile(f'{final_location}', codec='libx264')

        return final_location
