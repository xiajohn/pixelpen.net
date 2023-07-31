from blogPipeline.main import writeBlogs
from recurringTasks.email.main import sendEmails
from recurringTasks.social_media.facebookCreator import createFacebookPost
from common.makememe.make import make
from common.video.video_generator import makeVideo
from clients.midjourney_api import MidjourneyApi
import moviepy.config as mpconfig
from common.video.video_uploader import upload_video
mpconfig.change_settings({"IMAGEMAGICK_BINARY": r"C:\Program Files\ImageMagick-7.1.1-Q16-HDRI\magick.exe"})
if __name__ == "__main__":
    writeBlogs()
    
   # MidjourneyApi("product advertising", "video/how-to-market-your-product/images/image2.png")

