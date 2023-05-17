# todo: move memes to the DB and load them all into one prompt class as objects
# get rid of individual classes for memes
from PIL import Image
from common.makememe.generator.design.image_manager import Image_Manager
import os
class Prompt:
    def __init__(self, instruction, description):
        self.instruction = instruction

    def append_example(self, example):
        self.instruction = self.instruction + "Message:" + example + "\n" + "Meme:"

    def clean_user_input(self, user_input):
        cleaned_input = ''.join(char for char in user_input if char.isalnum())
        return cleaned_input

    def save_image(self, base, overlay_image, user_input):
        out = Image.alpha_composite(base, overlay_image)
        if out.mode in ("RGBA", "P"):
            out = out.convert("RGB")
        cleaned_input = self.clean_user_input(user_input)[:10]  # use the clean_user_input function
        image_name = f"{cleaned_input}.jpg"
        file_location = f"generated/memes/{image_name.replace(' ', '-')}"
        print(f'saving to {file_location}')
        out.save(file_location)
        return file_location




    def make_image(self, image_file_name, meme_text):
        print(f'meme text:{meme_text}')
        with Image.open(f"{self.get_base_image(image_file_name)}").convert(
            "RGBA"
        ) as base:
            return base
            

    def get_base_image(self, image_file_name):
        current_dir = os.path.dirname(os.path.abspath(__file__))
        base_dir = os.path.dirname(os.path.dirname(current_dir))  # Go up two levels from the current directory
        image_file_name = f"{self.name.lower().strip()}.jpg"
        return os.path.join(base_dir, "static", "meme_pics", image_file_name)
