from common.makememe.generator.prompts.prompt import Prompt
import datetime
from PIL import Image
from common.makememe.generator.design.image_manager import Image_Manager


class Accurate_Depiction(Prompt):
    id = 11
    name = "Accurate_Depiction"
    description = "accurate depiction"

    def __init__(self):
        self.instruction = """
###
Message:They told me I am too interested in crypto currencies and they couldn't be more right
Meme:{"depiction":"You are too interested in crypto currencies"}
###
Message:I had a fortune cookie tell me I code too much and It is so correct.
Meme:{"depiction":"You code too much"}
###
Message:You want to hear an accurate depiction. I am not running enough.
Meme:{"depiction":"You are not running enough"}
###
Message:They don't go outside enough. They need to get some sunlight. It's the truth
Meme:{"depiction":"They need to go outside more"}
###
Message:Humans making memes ok, AI making memes awesome.
Meme:{"depiction":"You want AI making memes"}
###
Message:Make a meme with strong and weak doggo comparing two types of pots
Meme:{"depiction":"strong and weak doggo comparing two types of pots"}
###
Message:Too much coffee
Meme:{"depiction":"You drink too much coffee"}
###
"""

    def create(self, meme_text, user_input):
        base = self.make_image(meme_text, user_input)
        
        overlay_image = Image_Manager.add_text(
            base=base,
            text=meme_text["depiction"],
            position=(275, 760),
            font_size=30,
            wrapped_width=25,
            rotate_degrees=350,
        )
        self.save_image(base, overlay_image, user_input)
        