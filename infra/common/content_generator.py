import openai
from unidecode import unidecode
import os
from PIL import Image, ImageDraw, ImageFont
import textwrap
import base64
import io
import random
from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv('../.env'))
        
class ContentGenerator:
    def __init__(self):
        openai.api_key = os.getenv("OPENAI_API_KEY")

    def generate_text(self, prompt, max_tokens=2500, temperature=0.7, retries=3):
        for _ in range(retries):
            try:
                response = openai.ChatCompletion.create(
                    model="gpt-3.5-turbo",
                    max_tokens=max_tokens,
                    temperature=temperature,
                    messages=[
                        {
                            "role": "system",
                            "content": "When it comes to writing content, two factors are crucial, perplexity and burstiness. Perplexity measures the complexity of text. Separately, burstiness compares the variations of sentences. Humans tend to write with greater burstiness, for example, with some longer or complex sentences alongside shorter ones. AI sentences tend to be more uniform. Therefore, when writing the following content I am going to ask you to create, I need it to have a good amount of perplexity and burstiness.",
                        },
                        {
                            "role": "user",
                            "content": prompt
                        }

                    ]
                )
                generated_text = response.choices[0].message.content
                clean_text = unidecode(generated_text)
                return clean_text
            except openai.error.APIError as e:
                if 'safety' in str(e):
                    prompt = f"Write a response on a safer version of the topic {prompt} without giving any options or lists."
                else:
                    raise e
        raise Exception("Failed to generate text after multiple retries")

    def generate_image(self, prompt, retries=3):
        base64_image_data_list = []

        for _ in range(retries):
            try:
                response = openai.Image.create(
                    prompt=prompt, n=1, size="256x256", response_format="b64_json")
                for data_object in response['data']:
                    base64_image_data = data_object['b64_json']
                    base64_image_data_list.append(base64_image_data)

                if base64_image_data_list:
                    # If the list is not empty, the image was generated successfully
                    break
            except openai.error.APIError as e:
                if 'safety' in str(e):
                    # Modify the prompt to make it safer
                    prompt = f"Generate an image for a safer version of the topic {prompt}"
                else:
                    # If it's not a safety-related error, raise the exception
                    raise e
        else:
            raise Exception("Failed to generate image after multiple retries")

        # If you only need the first image data, you can return the first item in the list
        return base64_image_data_list[0]

    def create_meme(self, output_path):
        meme_topics = [
            "cats",
            "dogs",
            "movies",
            "videogames",
            "sports",
            "celebrities",
            "music",
            "tv shows",
            "travel",
            "food",
            "technology",
            "work",
            "school",
        ]
        meme_topic = random.choice(meme_topics)
        meme_idea = self.generate_text(f"Generate a popular meme idea related to {meme_topic}")
        caption = self.generate_text(
            f"Create a funny caption for a meme about {meme_idea}. Please provide only the caption text without including the word 'caption'."
        )
        image_data = self.generate_image(meme_idea)
        img = self.load_image_from_base64(image_data)
        img_with_caption = self.add_caption_to_image(img, caption)
        img_with_caption.save(output_path)

    @staticmethod
    def load_image_from_base64(image_data):
        image_data = base64.b64decode(image_data)
        img = Image.open(io.BytesIO(image_data))
        return img

    @staticmethod
    def draw_text_with_outline(draw, x, y, text, font, fill, outline_thickness, outline_color):
        for dx in range(-outline_thickness, outline_thickness + 1):
            for dy in range(-outline_thickness, outline_thickness + 1):
                draw.text((x + dx, y + dy), text, font=font, fill=outline_color)
        draw.text((x, y), text, font=font, fill=fill)

    def add_caption_to_image(self, img, caption):
        draw = ImageDraw.Draw(img)
        img_width, img_height = img.size

        font_size = 30
        font = ImageFont.load_default()

        margin = 10
        max_width = img_width - 2 * margin
        wrapped_caption = textwrap.fill(caption, width=max_width // font_size)

        text_width, text_height = draw.textsize(wrapped_caption, font)
        x = (img_width - text_width) // 2
        y = img_height - text_height - margin

        # Split the wrapped caption into lines
        lines = wrapped_caption.split("\n")

        # Draw the text on the image
        for line_num, line in enumerate(lines):
            line_x = x
            line_y = y + line_num * text_height
            self.draw_text_with_outline(draw, line_x, line_y, line, font, (255, 255, 255), 2, (0, 0, 0))

        return img
    
# cg = ContentGenerator()
# output_path = "generated/output_meme.jpg"
# cg.create_meme(output_path)