from blogPipeline.main import writeBlogs
from recurringTasks.email.main import sendEmails
from recurringTasks.social_media.facebookCreator import createFacebookPost
from common.makememe.make import make
if __name__ == "__main__":
    #sendEmails()
    make("When your alarm goes off and you have to go to work because you didn't win the lottery")
