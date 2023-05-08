from blogPipeline.main import writeBlogs
from recurringTasks.email.main import sendEmails
from recurringTasks.social_media.facebookCreator import createFacebookPost
if __name__ == "__main__":
    createFacebookPost()
