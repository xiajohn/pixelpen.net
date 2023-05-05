from googlesearch import search
import requests
import re
from bs4 import BeautifulSoup
from urllib.parse import urljoin

class BlogCrawler:
    def __init__(self, query, num_results):
        self.query = query
        self.num_results = num_results
        self.blogs = self.get_blog_links()

    def get_blog_links(self):
        links = [j for j in search(self.query, num_results=self.num_results)]
        return links

    @staticmethod
    def is_valid_email(email):
        email_regex = re.compile(r"[^@]+@[^@]+\.[^@]+")
        return email_regex.match(email)
    
    def extract_emails(self, url):
        response = requests.get(url)
        soup = BeautifulSoup(response.text, "html.parser")

        contact_links = [url]  # Add the homepage URL to the list
        keywords = ["contact", "contact us"]

        for link in soup.find_all("a", href=True):
            if any(keyword in link["href"].lower() for keyword in keywords) and not link["href"].startswith("mailto:"):
                contact_links.append(urljoin(url, link["href"]))

        emails = []
        for link in contact_links:
            response = requests.get(link)
            soup = BeautifulSoup(response.text, "html.parser")
            for mailto_link in soup.select('a[href^="mailto:"]'):
                email = mailto_link['href'][7:]
                email = email.split('?')[0]
                if self.is_valid_email(email) and email not in emails:
                    emails.append(email)

        return emails


    

    def run(self):
        for blog in self.blogs:
            emails = self.extract_emails(blog)
            if len(emails) > 0:
                print(f"Emails found in {blog}: {emails}")

if __name__ == "__main__":
    crawler = BlogCrawler("food blog", 30)
    crawler.run()