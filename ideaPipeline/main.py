from blog_generator import BlogGenerator
from affiliate_link_injector import AffiliateLinkInjector

topics = [
    "Top 5 Thriller books 2023",
    "Best Science Fiction Books of 2023",
    "Top 5 Romance Novels to Read in 2023",
    "Top 5 Authors 2023",
    "Best Writers of 2023",
    "Top 5 Scary Novels to Read in 2023",
]

affiliate_links = [
    {"name": "Product 1", "url": "https://amzn.to/41QYLqy"},
    {"name": "Product 2", "url": "https://amzn.to/3n8ukNL"},
    {"name": "Product 3", "url": "https://amzn.to/3n8ukNL"},
]



for topic in topics:
    blog_generator = BlogGenerator(topic)
    blog_generator.create()

    affiliate_link_injector = AffiliateLinkInjector(blog_generator, affiliate_links)
    affiliate_link_injector.inject_links()


# Do something with generated_blogs, e.g., save to a file or print
