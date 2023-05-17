import requests
import os
from random import choice
from common.content_generator import ContentGenerator
from dotenv import load_dotenv, find_dotenv
from common.makememe.make import make
load_dotenv(find_dotenv('../.env'))
import json
class FacebookCreator(ContentGenerator):
    def __init__(self):
        super().__init__()
        self.page_id = "121834987557525"
        self.access_token = os.getenv("FACEBOOK_ACCESS_KEY")
        self.title_dict = {
            "practical tip": "💡 Practical Tip of the Day 💡",
            "funny joke": "😂 Funny Joke of the Day 😂",
            "interesting question": "🤔 Interesting Question of the Day 🤔"
        }
        self.hashtag_dict = {
            "practical tip": "#PracticalTips #UsefulInfo #LifeHacks",
            "funny joke": "#FunnyJokes #Humor #Laughter",
            "interesting question": "#InterestingQuestions #ThoughtProvoking #Curiosity"
        }

    def generate_title(self, category):
        return self.title_dict[category]

    def generate_hashtags(self, category):
        return self.hashtag_dict[category]

    def generate_text_content(self):
        category_prompts = {
            "practical tip": "Share a practical tip for anything. Limit response to only the practical tip. ",
            "funny joke": "Tell a funny joke. Limit response to only the funny joke. ",
            "interesting question": "Ask an interesting question about any topic. Limit response to only the interesting question. "
        }

        category = choice(list(category_prompts.keys()))
        selected_prompt = category_prompts[category] + "Limit response to less than 100 words"
        print(f'generating text for {selected_prompt}')
        response = self.generate_text(selected_prompt, max_tokens=200, temperature=1)
        title = self.generate_title(category)
        hashtags = self.generate_hashtags(category)

        return title, response.strip(), hashtags
    

    def upload_image(self, image_path):
        url = f"https://graph.facebook.com/{self.page_id}/photos"
        payload = {
            "access_token": self.access_token,
            "published": "false"
        }
        files = {
            "source": open(image_path, "rb")
        }
        
        response = requests.post(url, data=payload, files=files)
        result = json.loads(response.text)
        if 'id' in result:
            return result['id']
        else:
            raise Exception("Unable to upload image to Facebook")

    def create_facebook_post_with_image(self, content, image_id):
        url = f"https://graph.facebook.com/{self.page_id}/feed"
        payload = {
            "message": content,
            "attached_media": json.dumps([{"media_fbid": image_id}]),
            "access_token": self.access_token
        }
        
        response = requests.post(url, data=payload)
        return response.json()

    def create_facebook_post(self, content):
        url = f"https://graph.facebook.com/{self.page_id}/feed"
        payload = {
            "message": content,
            "access_token": self.access_token
        }

        response = requests.post(url, data=payload)
        return response.json()
    
    def get_image_prompt(self, content):
        return f'Generate a funny meme text for {content}'

    def post(self):
        
        # Generate title, text content, and hashtags
        title, text_content, hashtags = self.generate_text_content()
        imagePrompt = self.generate_text(self.get_image_prompt(text_content))
        print(f'image prompt: {imagePrompt}')
        # Generate an image
        image = make(imagePrompt)
        print(f'image path: {image}')
        image = self.upload_image(image)
        print(f'uploaded image {image}')
        # Construct Facebook post content
        tie_in_text = "Check out our blog for more insights: "
        post_content = f"{title}\n\n{text_content}\n\n{tie_in_text}\nhttps://www.pixelpen.net/creative-showcase\n\n#PixelPen {hashtags}"

        # Create the post
        print("Posting to Facebook:")
        print(post_content)
        post_result = self.create_facebook_post_with_image(post_content, image)
        print("Post result:", post_result)


def createFacebookPost():
    facebook_creator = FacebookCreator()
    facebook_creator.post()
