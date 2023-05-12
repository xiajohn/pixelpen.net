import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import re

class EmailExtractor:

    def extract_emails(self, url):
        contact_links = self.get_contact_links(url)
        return self.get_emails_from_links(contact_links)

    def get_contact_links(self, url):
        try:
            soup = self.get_soup(url)
        except Exception as e:
            print(f"Error fetching URL: {e}")
            return []

        contact_links = [url]  # Add the homepage URL to the list
        keywords = ["contact", "contact us"]

        for link in soup.find_all("a", href=True):
            if self.is_relevant_link(link, keywords) and not self.is_pdf(link):
                contact_links.append(urljoin(url, link["href"]))

        return contact_links

    def get_emails_from_links(self, contact_links):
        emails = []

        for link in contact_links:
            print(f'visiting {link}')
            try:
                soup = self.get_soup(link)
            except Exception as e:
                print(f"Error fetching contact link: {e}")
                continue

            for mailto_link in soup.select('a[href^="mailto:"]'):
                email = self.extract_email_from_mailto(mailto_link)
                if self.is_valid_email(email) and email not in emails:
                    emails.append(email)

        return emails

    def get_soup(self, url):
        response = requests.get(url)
        return BeautifulSoup(response.text, "html.parser")

    def is_relevant_link(self, link, keywords):
        return any(keyword in link["href"].lower() for keyword in keywords) and not link["href"].startswith("mailto:")

    def is_pdf(self, link):
        return link["href"].lower().endswith(".pdf")

    def extract_email_from_mailto(self, mailto_link):
        email = mailto_link['href'][7:]
        return email.split('?')[0]

    def is_valid_email(self, email):
        # Replace the following line with your preferred email validation method
        return re.match(r"[^@]+@[^@]+\.[^@]+", email)
