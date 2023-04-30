from blog_generator import BlogGenerator
from affiliate_link_injector import AffiliateLinkInjector

topic = "Top 5 Mystery books 2023"
affiliate_links = [
    {"name": "Product 1", "url": "https://amzn.to/41QYLqy"},
    {"name": "Product 2", "url": "https://amzn.to/3n8ukNL"},
    {"name": "Product 3", "url": "https://amzn.to/3n8ukNL"},
]

blog_generator = BlogGenerator(topic)
blog_generator.create()

affiliate_link_injector = AffiliateLinkInjector(blog_generator, affiliate_links)
affiliate_link_injector.inject_links()
