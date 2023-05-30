from blogPipeline.main import writeBlogs
from recurringTasks.email.main import sendEmails
from recurringTasks.social_media.facebookCreator import createFacebookPost
from common.makememe.make import make
from common.video.video_generator import makeVideo
if __name__ == "__main__":
    makeVideo()

