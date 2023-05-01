from blog_generator import BlogGenerator
from affiliate_link_injector import AffiliateLinkInjector
from build import build, clean_generated_folder
from internal_link_injector import InternalLinkInjector
from utils import TopicType

categories = {
    "pillows": {
        "topics": [
            {"topic": "Top 5 pillows in 2023", "type": TopicType.TRANSACTIONAL},
            {"topic": "Best Pillows for your neck", "type": TopicType.INFORMATIONAL},
            {"topic": "Best arm pillow", "type": TopicType.INFORMATIONAL},
        ],
        "affiliate_links": [
            {"name": "Royal Therapy Memory Foam Pillow", "url": "https://amzn.to/3LFpUXQ"},
            {"name": "EIUE Hotel Collection Bed Pillows", "url": "https://amzn.to/3AHjAsH"},
            {"name": "Casper Sleep Original Pillow", "url": "https://amzn.to/3AGbUa3"},
        ],
    },
    "trash bags": {
        "topics": [
            {"topic": "Top 5 best trash bags 2023", "type": TopicType.TRANSACTIONAL},
            {"topic": "Good trash bags", "type": TopicType.INFORMATIONAL},
            {"topic": "Cheap trash bags", "type": TopicType.TRANSACTIONAL},
            {"topic": "Moving with trash bags", "type": TopicType.INFORMATIONAL},
        ],
        "affiliate_links": [
            {"name": "Glad Tall Kitchen Trash Bags", "url": "https://amzn.to/41SksGN"},
            {"name": "GREENER WALKER 100% Compostable Trash Bags", "url": "https://amzn.to/41RlRxc"},
            {"name": "Top Knot Bags 45 Gallon Garbage Trash Bag 40X46", "url": "https://amzn.to/3HqMJvS"},
        ],
    },
    "honey": {
        "topics": [
            {"topic": "Best honey in 2023", "type": TopicType.TRANSACTIONAL},
            {"topic": "Benefits of honey", "type": TopicType.INFORMATIONAL},
            {"topic": "Are bees dying", "type": TopicType.INFORMATIONAL},
            {"topic": "How to make honey", "type": TopicType.INFORMATIONAL},
        ],
        "affiliate_links": [
            {"name": "Nature Nate's 100% Pure Organic", "url": "https://amzn.to/3LEZ6aj"},
            {"name": "Wedderspoon Raw Organic Manuka Honey", "url": "https://amzn.to/40Tyh6q"},
            {"name": "Florida Raw Apiaries", "url": "https://amzn.to/3VgRv4Y"},
        ],
    }
}


def clean_files(topic_list):
    clean_generated_folder(topic_list)


def process_categories(categories):
    blog_metadata = {}

    for category_name, category_data in categories.items():
        topics = category_data["topics"]
        affiliate_links = category_data["affiliate_links"]

        for topic_data in topics:
            topic = topic_data["topic"]
            type = topic_data["type"]
            blog_generator = BlogGenerator(topic)
            blog_folder = blog_generator.create()

            metadata = blog_generator.generate_metadata(topic)
            blog_metadata[topic] = metadata

            affiliate_link_injector = AffiliateLinkInjector(affiliate_links)
            if type == TopicType.TRANSACTIONAL:
                affiliate_link_injector.inject_links(blog_folder)

    return blog_metadata


def main(categories):
    blog_metadata = process_categories(categories)
    all_topics = [topic_data["topic"] for category_data in categories.values() for topic_data in category_data["topics"]]
    clean_files(all_topics)

    internal_link_injector = InternalLinkInjector(categories)
    internal_link_injector.inject_links()
    build(blog_metadata)


if __name__ == "__main__":
    main(categories)
