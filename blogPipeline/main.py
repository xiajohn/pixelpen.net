from blog_generator import BlogGenerator
from affiliate_link_injector import AffiliateLinkInjector
from build import build, clean_generated_folder
from internal_link_injector import InternalLinkInjector
from utils import TopicType, load_blog_metadata, save_blog_metadata
from blog_reviewer import BlogReviewer
import os
import openai
openai.api_key = os.getenv("OPENAI_API_KEY")
categories = {
    # "pillows": {
    #     "topics": [
    #         {"topic": "Top 5 pillows in 2023", "type": TopicType.TRANSACTIONAL},
    #         {"topic": "Best Pillows for your neck", "type": TopicType.INFORMATIONAL},
    #         {"topic": "Best arm pillow", "type": TopicType.INFORMATIONAL},
    #     ],
    #     "affiliate_links": [
    #         {"name": "Royal Therapy Memory Foam Pillow", "url": "https://amzn.to/3LFpUXQ"},
    #         {"name": "EIUE Hotel Collection Bed Pillows", "url": "https://amzn.to/3AHjAsH"},
    #         {"name": "Casper Sleep Original Pillow", "url": "https://amzn.to/3AGbUa3"},
    #     ],
    # },
    # "trash bags": {
    #     "topics": [
    #         {"topic": "Reliable trash bags 2023", "type": TopicType.TRANSACTIONAL},
    #         {"topic": "Good trash bags", "type": TopicType.INFORMATIONAL},
    #         {"topic": "Cheap trash bags", "type": TopicType.TRANSACTIONAL},
    #         {"topic": "Moving with trash bags", "type": TopicType.INFORMATIONAL},
    #     ],
    #     "affiliate_links": [
    #         {"name": "Glad Tall Kitchen Trash Bags", "url": "https://amzn.to/41SksGN"},
    #         {"name": "GREENER WALKER 100% Compostable Trash Bags", "url": "https://amzn.to/41RlRxc"},
    #         {"name": "Top Knot Bags 45 Gallon Garbage Trash Bag 40X46", "url": "https://amzn.to/3HqMJvS"},
    #     ],
    # },
    # "honey": {
    #     "topics": [
    #         {"topic": "Best honey in 2023", "type": TopicType.TRANSACTIONAL},
    #         {"topic": "Benefits of honey", "type": TopicType.INFORMATIONAL},
    #         {"topic": "Are bees dying", "type": TopicType.INFORMATIONAL},
    #         {"topic": "How to make honey", "type": TopicType.INFORMATIONAL},
    #     ],
    #     "affiliate_links": [
    #         {"name": "Nature Nate's 100% Pure Organic", "url": "https://amzn.to/3LEZ6aj"},
    #         {"name": "Wedderspoon Raw Organic Manuka Honey", "url": "https://amzn.to/40Tyh6q"},
    #         {"name": "Florida Raw Apiaries", "url": "https://amzn.to/3VgRv4Y"},
    #     ],
    # },
    # "soil": {
    #     "topics": [
    #         {"topic": "Best ways to test soil", "type": TopicType.TRANSACTIONAL},
    #         {"topic": "Soil ecosystem", "type": TopicType.TRANSACTIONAL},
    #         {"topic": "Save the soil", "type": TopicType.TRANSACTIONAL},
    #         {"topic": "Better soil", "type": TopicType.TRANSACTIONAL},
    #     ],
    #     "affiliate_links": [
    #         {"name": "Soil Testing", "url": "https://salemsoilsolutions.com"},
    #         {"name": "Brut Worm Castings ", "url": "https://amzn.to/3LlWs7X"},
    #         {"name": "The Andersons HumiChar Organic Soil", "url": "https://amzn.to/41XWJoU"},
    #     ],
    # },
    "summer": {
        "topics": [
            {"topic": "Best products summer 2023", "type": TopicType.TRANSACTIONAL},
            {"topic": "Beach Essentials 2023", "type": TopicType.TRANSACTIONAL},
            {"topic": "Summer trends 2023", "type": TopicType.TRANSACTIONAL},
            {"topic": "What to do this summer", "type": TopicType.INFORMATIONAL},
            {"topic": "Summer Essentials", "type": TopicType.TRANSACTIONAL},
            {"topic": "Sun damage to skin", "type": TopicType.INFORMATIONAL},
            {"topic": "What Sunburn does to your skin", "type": TopicType.INFORMATIONAL},
        ],
        "affiliate_links": [
            {"name": "FURTALK Sun Visor Hats", "url": "https://amzn.to/3Lp8Bce"},
            {"name": "NPJY Bucket Hat for Women Men  ", "url": "https://amzn.to/3LHPdZr"},
             {"name": "Gildan A-Shirt Tanks", "url": "https://amzn.to/3nfAFGX"},
            {"name": "Neutrogena Beach Defense Water-Resistant", "url": "https://amzn.to/3LiLWyd"},
        ],
    },
    # "bbq": {
    #     "topics": [
    #         {"topic": "Best bbq summer 2023", "type": TopicType.TRANSACTIONAL},
    #          {"topic": "Grill Hacks 2023", "type": TopicType.TRANSACTIONAL},
    #          {"topic": "Summer grilling 2023", "type": TopicType.TRANSACTIONAL},
    #          {"topic": "What to grill", "type": TopicType.TRANSACTIONAL},
    #          {"topic": "Is grilling healthy for you", "type": TopicType.INFORMATIONAL},
    #          {"topic": "How to choose a grill", "type": TopicType.INFORMATIONAL},
    #     ],
    #     "affiliate_links": [
    #         {"name": "Royal Gourmet CC1830F Charcoal Grill", "url": "https://amzn.to/3NzkgYV"},
    #         {"name": "American Gourmet 463672717  ", "url": "https://amzn.to/41TbitP"},
    #          {"name": "Grill brush", "url": "https://amzn.to/44gZwef"},
    #         {"name": "GRILLART Grill Brush and Scraper", "url": "https://amzn.to/3LK2f8D"},
    #     ],
    # }
}

def process_categories(categories):
    blog_metadata = load_blog_metadata()

    for category_name, category_data in categories.items():
        topics = category_data["topics"]
        affiliate_links = category_data["affiliate_links"]

        for topic_data in topics:
            topic = topic_data["topic"]
            type = topic_data["type"]

            if topic not in blog_metadata:
                blog_generator = BlogGenerator(topic)
                blog_folder = blog_generator.create()

                metadata = blog_generator.generate_metadata(topic)
                blog_metadata[topic] = metadata

                affiliate_link_injector = AffiliateLinkInjector(affiliate_links)
                if type == TopicType.TRANSACTIONAL:
                    affiliate_link_injector.inject_links(blog_folder)

    save_blog_metadata(blog_metadata)
    return blog_metadata


def main(categories):
    blog_metadata = process_categories(categories)
    all_topics = [topic_data["topic"] for category_data in categories.values() for topic_data in category_data["topics"]]
    clean_generated_folder(all_topics)

    internal_link_injector = InternalLinkInjector(categories)
    internal_link_injector.inject_links()

    # Call the build function with the loaded blog_metadata
    build(blog_metadata)




if __name__ == "__main__":
    main(categories)
