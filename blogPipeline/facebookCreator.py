import requests
import os
import time
from dotenv import load_dotenv
from random import choice
from utils import load_blog_metadata
from content_generator import ContentGenerator

load_dotenv()

class FacebookCreator(ContentGenerator):
    def __init__(self):
        super().__init__()
        self.page_id = "121834987557525"
        self.access_token = os.getenv("FACEBOOK_ACCESS_KEY")
        self.blog_metadata = load_blog_metadata()

    def generate_question_and_response(self):
        prompt = "Share a practical tip for anything"
        question_and_response = self.generate_text(prompt, max_tokens=100)
        return question_and_response.strip()

    def get_random_blog_links(self, num_links=2):
        blog_keys = list(self.blog_metadata.keys())
        random_keys = [choice(blog_keys) for _ in range(num_links)]
        blog_links = [f"https://www.pixelpen.net/blog/{key.replace(' ', '-')}" for key in random_keys]
        return blog_links

    def create_facebook_post(self, content):
        url = f"https://graph.facebook.com/{self.page_id}/feed"
        payload = {
            "message": content,
            "access_token": self.access_token
        }

        response = requests.post(url, data=payload)
        return response.json()

    def post_twice_daily(self):
        while True:
            # Generate question and response
            question_and_response = self.generate_question_and_response()

            # Generate random blog links
            random_blog_links = self.get_random_blog_links()

            # Construct Facebook post content
            tie_in_text = "At Pixel Pen, we're committed to crafting excellence, one idea at a time. Check out our blog for more insights: "
            post_content = f"{question_and_response}\n\n{tie_in_text}\n{random_blog_links[0]}\n{random_blog_links[1]}"

            # Create the post
            print("Posting to Facebook:")
            print(post_content)
            post_result = self.create_facebook_post(post_content)
            print("Post result:", post_result)

            # Wait 12 hours before posting again
            time.sleep(12 * 60 * 60)

if __name__ == "__main__":
    facebook_creator = FacebookCreator()
    facebook_creator.post_twice_daily()
