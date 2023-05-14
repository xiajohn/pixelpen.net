from blogPipeline.main import writeBlogs
from recurringTasks.email.main import sendEmails
from recurringTasks.social_media.facebookCreator import createFacebookPost
from recurringTasks.makememe.make import make
if __name__ == "__main__":
    make("lost something")
