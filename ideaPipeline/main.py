from blog_generator import BlogGenerator
from affiliate_link_injector import AffiliateLinkInjector
from build import build, clean_generated_folder

categories = {
    "fashion": {
        "topics": [
            {"topic": "Top 5 cars 2023", "type": "transactional"},
        ],
        "affiliate_links": [
            {"name": "Dawn Girl", "url": "https://amzn.to/41QYLqy"},
            {"name": "Foreign Deceit", "url": "https://amzn.to/3n8ukNL"},
            {"name": "The Worst Wedding Date", "url": "https://amzn.to/41QYLqy"},
        ],
    },
}


blog_metadata = {}

# Iterate through categories
for category_name, category_data in categories.items():
    
    topics = category_data["topics"]
    affiliate_links = category_data["affiliate_links"]
    #clean_generated_folder([topic_data["topic"] for topic_data in topics])
    for topic_data in topics:
        topic = topic_data["topic"]
        type = topic_data["type"]
        blog_generator = BlogGenerator(topic)
        blog_folder = blog_generator.create()

        # Generate metadata for the blog
        metadata = blog_generator.generate_metadata(topic)

        # Store metadata in the blog_metadata dictionary
        blog_metadata[topic] = metadata

        affiliate_link_injector = AffiliateLinkInjector(affiliate_links)
        if type == "transactional":
            affiliate_link_injector.inject_links(blog_folder)

# Call the build function with the generated blog_metadata
build(blog_metadata)
