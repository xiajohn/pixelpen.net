import requests
import os
from random import choice
from common.utils import load_json
from ...common.content_generator import ContentGenerator
from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv('../.env'))


class FacebookCreator(ContentGenerator):
    def __init__(self):
        super().__init__()
        self.page_id = "121834987557525"
        self.access_token = os.getenv("FACEBOOK_ACCESS_KEY")
        self.blog_metadata = load_json("blog_metadata.json")

    def generate_question_and_response(self):
        prompts = [
            "Share a practical tip for anything",
            "Tell a funny joke",
            "Ask an interesting question about any topic"
        ]

        selected_prompt = choice(prompts) + "Limit response to less than 100 words"
        question_and_response = self.generate_text(selected_prompt, max_tokens=200)
        return question_and_response.strip()

    def create_facebook_post(self, content):
        url = f"https://graph.facebook.com/{self.page_id}/feed"
        payload = {
            "message": content,
            "access_token": self.access_token
        }

        response = requests.post(url, data=payload)
        return response.json()
    


    def post_twice_daily(self):
        
        # Generate question and response
        question_and_response = self.generate_question_and_response()

        # Construct Facebook post content
        tie_in_text = "At Pixel Pen, we're committed to crafting excellence, one idea at a time. Check out our blog for more insights: "
        post_content = f"{question_and_response}\n\n{tie_in_text}\nhttps://www.pixelpen.net/creative-showcase"

        # Create the post
        print("Posting to Facebook:")
        print(post_content)
        post_result = self.create_facebook_post(post_content)
        print("Post result:", post_result)

if __name__ == "__main__":
    facebook_creator = FacebookCreator()
    facebook_creator.post_twice_daily()
