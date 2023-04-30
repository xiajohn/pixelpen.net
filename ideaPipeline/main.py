from blog_generator import BlogGenerator

topic = "Top 5 Mystery books 2023"
affiliate_links = [
    {"name": "Product 1", "url": "https://your-affiliate-link-1"},
    {"name": "Product 2", "url": "https://your-affiliate-link-2"},
    {"name": "Product 3", "url": "https://your-affiliate-link-3"},
]

blog_generator = BlogGenerator(topic)
blog_generator.create()
#blog_generator.inject_affiliate_links(affiliate_links)
