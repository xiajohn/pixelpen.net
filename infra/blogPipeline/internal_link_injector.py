import os
import random
from utils import TopicType
import re
class InternalLinkInjector:
    def __init__(self, categories, generated_folder="generated"):
        self.categories = categories
        self.generated_folder = generated_folder

    def get_links_for_topic(self, topic_data, num_links, category):
        topic_type = topic_data["type"]
        topic = topic_data["topic"]

        all_topics = self.categories[category]["topics"]
        other_topics = [t for t in all_topics if t["topic"] != topic]

        if topic_type == "INFORMATIONAL":
            transactional_topics = [t for t in other_topics if t["type"] == "TRANSACTIONAL"]
            if transactional_topics:
                random.shuffle(transactional_topics)
                other_topics = transactional_topics + other_topics

        random.shuffle(other_topics)

        return other_topics[:num_links]

    def add_links_to_blog_post(self, blog_folder, links):
        blog_post_path = os.path.join(blog_folder, "blog_post.md")

    # Check if the blog post file exists
        if not os.path.isfile(blog_post_path):
            print(f"Blog post '{blog_post_path}' does not exist. Skipping link injection.")
            return
        with open(blog_post_path, "r") as f:
            content = f.read()

        if "Other articles you may be interested in" in content:
            print(f"Internal links already exist in '{blog_post_path}'. Skipping link injection.")
            return
        links_md = "### Other articles you may be interested in\n\n"

        for link_data in links:
            link_topic = link_data["topic"]
            link_folder = link_topic.replace(" ", "-")
            links_md += f"- [{re.sub(r'<[^>]*>', '', link_topic)}]({link_folder})\n"

        content += "\n" + links_md

        with open(blog_post_path, "w") as f:
            f.write(content)



    def inject_links(self):
        for category, category_data in self.categories.items():
            topics = category_data["topics"]

            for topic_data in topics:
                topic = topic_data["topic"]
                folder_name = topic.replace(" ", "-")
                blog_folder = os.path.join(self.generated_folder, folder_name)

                # Find the number of links to inject
                num_links = min(4, len(topics) - 1)

                # Generate a list of links based on the current topic and its type
                links = self.get_links_for_topic(topic_data, num_links, category)

                # Inject the links into the blog post
                self.add_links_to_blog_post(blog_folder, links)