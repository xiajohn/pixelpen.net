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

    def make_image(self, image_file_name, meme_text, user_input):
        print(f'meme text:{meme_text}')
        with Image.open(f"{self.get_base_image(image_file_name)}").convert(
            "RGBA"
        ) as base:
            overlay_image = Image_Manager.add_text(
                base=base,
                text=next(iter(meme_text.values())),
                position=(425, 950),
                font_size=40,
                wrapped_width=15,
            )
            out = Image.alpha_composite(base, overlay_image)
            if out.mode in ("RGBA", "P"):
                out = out.convert("RGB")
                image_name = f"{user_input}.jpg"
                file_location = f"{image_name}"
                print(f'saving to {file_location}')
                out.save(file_location)
                return image_name

    def get_base_image(self, image_file_name):
        current_dir = os.path.dirname(os.path.abspath(__file__))
        base_dir = os.path.dirname(os.path.dirname(current_dir))  # Go up two levels from the current directory
        image_file_name = f"{self.name.lower().strip()}.jpg"
        return os.path.join(base_dir, "static", "meme_pics", image_file_name)
