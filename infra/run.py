from blogPipeline.main import writeBlogs
from recurringTasks.email.main import sendEmails
from recurringTasks.social_media.facebookCreator import createFacebookPost
from common.makememe.make import make
if __name__ == "__main__":
    createFacebookPost()
    #make("They dont know ai can make memes")
