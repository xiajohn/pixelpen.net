from blogPipeline.main import writeBlogs
from recurringTasks.email.main import sendEmails
from recurringTasks.social_media.facebookCreator import createFacebookPost
from common.makememe.make import make
from common.video.video_generator import makeVideo
from clients.midjourney_api import MidjourneyApi
if __name__ == "__main__":
    MidjourneyApi("product marketting", "video/how-to-market-your-product/images/image1.png")

