from blog_generator import BlogGenerator
from affiliate_link_injector import AffiliateLinkInjector
from build import build

topics = [
    "Top 5 fashion trends 2023",
    "Best dresses of 2023",
    "Top 5 tank tops in 2023",
    "Top 5 shoes 2023",
    "Best fashion of 2023"
]

affiliate_links = [
    {"name": "Dawn Girl", "url": "https://amzn.to/41QYLqy"},
    {"name": "Foreign Deceit", "url": "https://amzn.to/3n8ukNL"},
    {"name": "The Worst Wedding Date", "url": "https://amzn.to/41QYLqy"},
]

blog_metadata = {}

for topic in topics:
    blog_generator = BlogGenerator(topic)
    blog_generator.create()

    # Generate metadata for the blog
    metadata = blog_generator.generate_metadata(topic)

    # Store metadata in the blog_metadata dictionary
    blog_metadata[topic] = metadata

    affiliate_link_injector = AffiliateLinkInjector(blog_generator, affiliate_links)
    affiliate_link_injector.inject_links()

# Call the build function with the generated blog_metadata
build(blog_metadata)
