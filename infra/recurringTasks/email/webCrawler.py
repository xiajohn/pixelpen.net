
import re
import random
from googleapiclient.discovery import build
from common.content_generator import ContentGenerator
from recurringTasks.email.emailExtractor import EmailExtractor
import os
from dotenv import load_dotenv, find_dotenv
import json

from urllib.parse import quote
load_dotenv(find_dotenv('../.env'))
class BlogCrawler(EmailExtractor):
    def __init__(self, num_results=30):
        self.num_results = num_results
        self.contentGenerator = ContentGenerator()

        categories = [
            "Technology",
            "Travel",
            "Food",
            "Lifestyle",
            "Health"
        ]
        category = random.choice(categories)
        self.topic = self.contentGenerator.generate_text(f"Generate a random title for {category}", 250, 1)

        self.blogs = self.get_blog_links()

    def get_blog_links(self):
        print(f'finding links for {self.topic}')
        service = build("customsearch", "v1", developerKey=os.getenv("GOOGLE_SEARCH_API_KEY")).cse()
        query = self.topic.replace('"', '')
        result = service.list(q=query, cx='e0642cb81e6904b7a').execute()
        all_links = [item['link'] for item in result['items']]
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


