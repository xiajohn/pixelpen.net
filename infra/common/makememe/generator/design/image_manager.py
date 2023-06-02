import traceback
from PIL import Image, ImageDraw, ImageFont, ImageOps, ImageChops
# from makememe.generator.design.font import font_path
from common.makememe.generator.prompts.helper import Helper
import os
import traceback, textwrap
import requests
from io import BytesIO
import random
from common.metadata_manager import MetadataManager
from common.video.constants import Constants
class Image_Manager:
    def __init__(self):
        print("Image manager create")
        self.metadata_manager = MetadataManager()

    @staticmethod
    def add_text(
        base,
        text,
        position,
        font_size,
        text_color="black",
        text_width_proportion=4,
        wrapped_width=None,
        rotate_degrees=None,
    ):
        try:
            overlay_image = Image.new("RGBA", base.size, (0, 0, 0, 0))
            if wrapped_width is not None:
                text = Helper.wrap(text, wrapped_width)

            current_path = os.path.dirname(os.path.abspath(__file__))
            font_path = os.path.join(current_path, "impact.ttf")
            font = ImageFont.truetype(font_path, font_size)
            draw = ImageDraw.Draw(overlay_image)
            fill = (0, 0, 0, 255)
            if text_color == "white":
                fill = (255, 255, 255, 255)
            draw.text(position, text, font=font, fill=fill)
            if rotate_degrees is not None:
                overlay_image = overlay_image.rotate(rotate_degrees)

            return overlay_image
        except Exception as e:
            print(f"Error occurred in add_text: {e}")
            traceback.print_exc()  # Print full exception stack trace
            raise  # Reraise the exception
    @staticmethod
    def download_image(query):
        try:
            # Query Pixabay API for an image
            api_key = os.getenv('PIXABAY_KEY')
            url = f'https://pixabay.com/api/?key={api_key}&q={query}&image_type=photo'
            response = requests.get(url).json()

            # Get the URL of the first image in the response
            image_url = random.choice(response['hits'][:5])['largeImageURL']


            # Download the image
            image_response = requests.get(image_url)
            img = Image.open(BytesIO(image_response.content))

            return img
        except Exception as e:
            print(f"Error occurred in download_image: {e}")
            traceback.print_exc()  # Print full exception stack trace
            raise  # Reraise the exception

    @staticmethod
    def add_text_with_shadow(img, text, position, font_size, text_color="white"):
        try:
            overlay_image = Image.new("RGBA", img.size, (0, 0, 0, 0))
            draw = ImageDraw.Draw(overlay_image)

            font_path = 'impact.ttf'
            font = ImageFont.truetype(font_path, font_size)
            
            # Break the text into two lines if it's too long
            max_length_per_line = 20  # or whatever length you think is best
            if len(text) > max_length_per_line:
                lines = textwrap.wrap(text, max_length_per_line)
                text = '\n'.join(lines)

            textwidth, textheight = draw.textsize(text, font)

            x, y = position

            # Draw a semi-transparent rectangle behind the text
            margin = 10
            rectangle_start = (x - margin, y - margin)
            rectangle_end = (x + textwidth + margin, y + textheight + margin)
            draw.rectangle((rectangle_start, rectangle_end), fill=(0, 0, 0, 128))

            # Draw the text with a slight shadow
            shadowcolor = "black"
            for shadow_position in [(x-1, y-1), (x+1, y-1), (x-1, y+1), (x+1, y+1)]:
                draw.text(shadow_position, text, font=font, fill=shadowcolor)

            # Draw the text
            draw.text((x, y), text, fill=text_color, font=font)

            return overlay_image
        except Exception as e:
            print(f"Error occurred in add_text_with_shadow: {e}")
            traceback.print_exc()  # Print full exception stack trace
            raise  # Reraise the exception


    @staticmethod
    def create_thumbnail_with_text(query, text, folder_path):
        if MetadataManager().check_metadata(Constants.thumbnail_image, folder_path):
            return
        try:
            img = Image_Manager.download_image(query)

            # Resize the image to YouTube's recommended size
            img = img.resize((1280, 720), Image.ANTIALIAS)

            font_size = 105

            # Fixed positions for the text
            positions = [ (360, 285), (360, 50), (60, 50)]

            # Randomly choose a position for the text
            position = random.choice(positions)

            overlay_image = Image_Manager.add_text_with_shadow(img, text, position, font_size)

            img_with_overlay = Image.alpha_composite(img.convert('RGBA'), overlay_image)
            img_with_overlay.convert('RGB').save(f'{folder_path}/{Constants.thumbnail}.jpg')

        except Exception as e:
            print(f"Error occurred in create_thumbnail_with_text: {e}")
            traceback.print_exc()  # Print full exception stack trace
            raise  # Reraise the exception
