
import re
from googlesearch import search
from common.content_generator import ContentGenerator
from recurringTasks.email.emailExtractor import EmailExtractor
class BlogCrawler(EmailExtractor):
    def __init__(self, num_results=30, topic="generate a random blog category. respond with only the title"):
        self.num_results = num_results
        self.contentGenerator = ContentGenerator()
        self.topic = self.contentGenerator.generate_text(topic, 250, 1)
        self.blogs = self.get_blog_links()

    def get_blog_links(self):
        print(f'sending emails to {self.topic}')
        all_links = [j for j in search(self.topic, num_results=self.num_results)]
        return all_links

    @staticmethod
    def is_valid_email(email):
        email_regex = re.compile(r"[^@]+@[^@]+\.[^@]+")
        return email_regex.match(email) and not email.endswith('.gov')

    def run(self):
        emailList = []
        for blog in self.blogs:
            emails = self.extract_emails(blog)
            if len(emails) > 0:
                emailList += emails[:3]
                print(f"Emails found in {blog}: {emails}")
        return emailList


