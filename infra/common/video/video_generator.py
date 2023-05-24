from moviepy.editor import concatenate_videoclips, VideoFileClip, AudioFileClip
import pixabay
import os

class VideoGenerator:
    def __init__(self, pixabay_key):
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
        for i in range(3):
            os.remove(f'space{i}.mp4')

        # Return the path to the final video clip
        return f'{query}_without_audio.mp4'

    def addAudio(self, video_path, audio_path):
        # Load the video
        final_clip = VideoFileClip(video_path)

        # Add the audio to the video
        audio = AudioFileClip(audio_path)
        final_clip = final_clip.set_audio(audio)

        # Write the result to a file
        final_clip.write_videofile(f'{video_path[:-4]}_with_audio.mp4', codec='libx264')

# usage:
vg = VideoGenerator("YOUR_PIXABAY_API_KEY")
# video_path = vg.getVideo(30, "nature")
vg.addAudio("nature_without_audio.mp4", "audio.wav")
