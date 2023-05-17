from common.makememe.generator.prompts.prompt import Prompt
import datetime
from PIL import Image
from common.makememe.generator.design.image_manager import Image_Manager
import os


class Scary(Prompt):
    id = 15
    name = "Scary"
    description = "scary"

    def __init__(self):
        self.instruction = """
###
Message:React Navtive scares me more than any other library I've ever used.
Meme:{"subject":"React Native"}
###
Message:I can't imagine having to run a marathon
Meme:{"subject":"marathons"}
###
"""

    def create(self, meme_text, user_input):
        base = self.make_image(meme_text, user_input)

        overlay_image = Image_Manager.add_text(
            base=base,
            text=meme_text["subject"],
            position=(425, 950),
            font_size=40,
            wrapped_width=15,
        )
        
        return self.save_image(base, overlay_image, user_input)
