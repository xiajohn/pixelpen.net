from recurringTasks.email.webCrawler import BlogCrawler
from recurringTasks.email.emailSender import EmailSender
def sendEmails():
    crawler = BlogCrawler("honey blogs", 10)
    emails = crawler.run()
    print(emails)

    email_sender = EmailSender()
    email_sender.send_emails(emails)