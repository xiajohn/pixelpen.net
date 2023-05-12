from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail, TrackingSettings, ClickTracking
import os
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv('../.env'))
sendgrid_api_key = os.getenv("SENDGRID_API_KEY")


class EmailSender:
    def __init__(self, sent_emails_file='recurringTasks/email/sent_emails.txt'):
        self.email_subject = "Collaboration Opportunities with Pixel Pen"
        self.email_content = """Hi there,

        I hope this message finds you well. My name is John, a software developer with a passion for content creation. I'm reaching out from Pixel Pen, a creative platform I've started. We craft engaging and innovative content with the help of AI assistance.

        As a fellow new blogger, I understand the challenges of consistently creating high-quality content and getting your blog to show up on search engines. I believe there is a lot of opportunity in the space of content creation and distribution, and I'm excited to explore ways we can collaborate and grow together.

        I came across your blog and was impressed by the content you've been publishing. I'd like to propose a collaboration where we could exchange links to be published on each other's websites. I can create a guest post for you. This would not only diversify your content but also increase exposure and drive traffic for both our blogs. I can add a link to your site from one of my blogs at no extra cost.

        If you're interested in this partnership or would like to explore other collaboration opportunities, please don't hesitate to reach out. I look forward to hearing from you and discussing how we can both grow in this exciting space. Feel free to explore my work at https://pixelpen.net/creative-showcase

        Best regards,

        John
        Pixel Pen
        """
        self.sent_emails_file = sent_emails_file

    def load_sent_emails(self):
        if not os.path.exists(self.sent_emails_file):
            return set()

        with open(self.sent_emails_file, 'r') as file:
            sent_emails = set(line.strip() for line in file.readlines())

        return sent_emails

    def save_sent_emails(self, sent_emails):
        with open(self.sent_emails_file, 'a') as file:
            for email in sent_emails:
                file.write(f"{email}\n")

    def send_email(self, to_email):
       #sent_emails = self.load_sent_emails()
        message = Mail(
            from_email=("pixel.pen3@gmail.com", "Pixel Pen"),
            to_emails=to_email,
            subject=self.email_subject,
            plain_text_content=self.email_content,
        )

        tracking_settings = TrackingSettings()
        click_tracking = ClickTracking(False, False)
        tracking_settings.click_tracking = click_tracking
        message.tracking_settings = tracking_settings

        try:
            sg = SendGridAPIClient(sendgrid_api_key)
            response = sg.send(message)

            print(f'email sent to {to_email} successfully')
        except Exception as e:
            print(f"Error sending email: {e}")

    def send_emails(self, emails):
        emails = list(set(emails))
        for email in emails:
            self.send_email(email)
        #self.save_sent_emails(emails)




