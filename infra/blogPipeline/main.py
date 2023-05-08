from blogPipeline.blog_generator import BlogGenerator
from blogPipeline.affiliate_link_injector import AffiliateLinkInjector
from blogPipeline.build import build, clean_generated_folder
from blogPipeline.internal_link_injector import InternalLinkInjector
from common.utils import TopicType, load_json, save_json
import os
import openai
openai.api_key = os.getenv("OPENAI_API_KEY")


def process_categories(categories):
    blog_metadata = load_json("../generated/blog_metadata.json")

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

                affiliate_link_injector = AffiliateLinkInjector(
                    affiliate_links)
                if type == TopicType.TRANSACTIONAL:
                    affiliate_link_injector.inject_links(blog_folder)

    save_json(blog_metadata, os.path.join("../generated/blog_metadata.json"))
    return blog_metadata


def writeBlogs():
    categories = load_json("../user_input.json")
    blog_metadata = process_categories(categories)
    all_topics = [topic_data["topic"] for category_data in categories.values()
                  for topic_data in category_data["topics"]]
    clean_generated_folder(all_topics)

    internal_link_injector = InternalLinkInjector(categories)
    internal_link_injector.inject_links()

    # Call the build function with the loaded blog_metadata
    build(blog_metadata)
