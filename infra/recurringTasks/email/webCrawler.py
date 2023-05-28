
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
    def __init__(self, num_results=60):
        self.num_results = num_results
        self.contentGenerator = ContentGenerator()

        categories = [
            "Technology",
            "Travel",
            "Food",
            "Movies",
            "TV shows",
            "Investing",
            "Seattle",
            "Business",
            "Video Games",
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
        
        all_links = []
        max_results = self.num_results  # Set the desired maximum number of results here
        results_per_page = 10  # Google Search API returns 10 results per page by default
        
        for page in range(1, max_results, results_per_page):
            try:
                result = service.list(q=query, cx='e0642cb81e6904b7a', start=page).execute()
                all_links.extend([item['link'] for item in result['items']])
            except Exception as e:
                print(f"Error fetching results for page {page}: {e}")
                break

        return all_links


    def run(self):
        emailList = []
        for blog in self.blogs:
            emails = self.extract_emails(blog)
            if len(emails) > 0:
                emailList += emails[:3]
                print(f"Emails found in {blog}: {emails}")
        return emailList


