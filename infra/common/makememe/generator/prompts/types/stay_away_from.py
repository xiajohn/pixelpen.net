from common.makememe.generator.prompts.prompt import Prompt
import datetime
from PIL import Image
from common.makememe.generator.design.image_manager import Image_Manager


class Stay_Away_From(Prompt):
    id = 13
    name = "Stay_Away_From"
    description = "stay away from"

    def __init__(self):
        self.instruction = """
###
Message:I typically prefer to stay away from people who are not my friends.
Meme:{"subject":"who are not my friends."}
###
Message:I don't hang out with Tiktokers
Meme:{"subject":"Tiktokers"}
###
"""

    def create(self, meme_text, user_input):
        base = self.make_image(meme_text, user_input)

        overlay_image = Image_Manager.add_text(
            base=base,
            text=meme_text["subject"],
            position=(115, 300),
            font_size=30,
            wrapped_width=15,
        )
        
        self.save_image(base, overlay_image, user_input)