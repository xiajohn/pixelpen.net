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
        contact_links = list(set(contact_links))
        keywords = ["contact", "contact us", "about"]

        for link in soup.find_all("a", href=True):
            if self.is_relevant_link(link, keywords) and not self.is_pdf(link):
                contact_links.append(urljoin(url, link["href"]))

        return contact_links

    def get_emails_from_links(self, contact_links):
        emails = []

        # Define the regex pattern for email addresses
        email_pattern = r'(?:[a-z0-9!#$%&\'*+/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&\'*+/=?^_`{|}~-]+)*|"(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21\x23-\x5b\x5d-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])*")@(?:(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?|\[(?:(?:(2(5[0-5]|[0-4][0-9])|1[0-9][0-9]|[1-9]?[0-9]))\.){3}(?:(2(5[0-5]|[0-4][0-9])|1[0-9][0-9]|[1-9]?[0-9])|[a-z0-9-]*[a-z0-9]:(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21-\x5a\x53-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])+)\])'
        contact_links = list(set(contact_links))
        for link in contact_links:
            print(f'visiting {link}')
            try:
                soup = self.get_soup(link)
            except Exception as e:
                print(f"Error fetching contact link: {e}")
                continue

            # Find emails in 'mailto' links
            for mailto_link in soup.select('a[href^="mailto:"]'):
                email = self.extract_email_from_mailto(mailto_link)
                if self.is_valid_email(email) and email not in emails:
                    emails.append(email)

            # Find emails using regex pattern in the soup's text content
            found_emails = re.findall(email_pattern, soup.get_text(), re.IGNORECASE)
            for email in found_emails:
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
        # Check if the input is a string, return False if not
        if not isinstance(email, str):
            return False

        return not email.endswith('.gov')

