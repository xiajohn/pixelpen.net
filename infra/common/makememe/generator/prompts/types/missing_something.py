from makememe.generator.prompts.prompt import Prompt
import datetime
from PIL import Image
from makememe.generator.design.image_manager import Image_Manager


class Missing_Something(Prompt):
    name = "Missing_Something"
    description = "something is missing and I wish it was still here"

    def __init__(self):
        self.instruction = """
###
Message:I miss going for long by the beach
Meme:{"missing": "long runs by the beach"}
###
Message:I wish there was a new season of The Office
Meme:{"missing": "a new season of The Office"}
###
Message:I love the smell of a new car
Meme:{"missing": "The smell of a brand new car"}
###
"""

    def create(self, meme_text, user_input):
        base = self.make_image(meme_text, user_input)

        overlay_image = Image_Manager.add_text(
            base=base,
            text=meme_text["missing"],
            position=(1150, 550),
            font_size=50,
            wrapped_width=12,
        )
        
        return self.save_image(base, overlay_image, user_input)
