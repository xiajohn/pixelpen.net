from common.makememe.generator.prompts.prompt import Prompt
import datetime
from PIL import Image
from common.makememe.generator.design.image_manager import Image_Manager


class No_Responsibility(Prompt):
    id = 8
    name = "No_Responsibility"
    description = "two parties blaming eachother for something"

    def __init__(self):
        self.instruction = """
###
Message:Company 1 is suing company 2 and neither thinks they are wrong
Meme:{"party_one":"Company 1", "party_two":"company 2"}
###
Message:The shoemaker blames the sockmaker and the sockmaker blames the shoemaker
Meme:{"party_one":"shoemaker", "party_two":"sockmaker"}
###
Message:Coffee blames tea for not waking me up after I drink both
Meme:{"party_one":"coffee blaming tea for not walking me up", "party_two":"tea"}
###
Message:I can't do anything useful
Meme:{"party_one":"me", "party_two":"me"}
###
Message:break
Meme:{"party_one":"break", "party_two":"break"}
###
Message:tlest;laksd
Meme:{"party_one":"test;laksd", "party_two":"test;laksd"}
###
Message:The code I wrote this week blames the code I wrote last week
Meme:{"party_one":"The code I wrote this week", "party_two":"the code I wrote last week"}
###
"""

    def create(self, meme_text, user_input):
        base = self.make_image(meme_text, user_input)

        overlay_image = Image_Manager.add_text(
            base=base,
            text=meme_text["party_one"],
            position=(175, 200),
            font_size=40,
            text_color="white",
            wrapped_width=12,
        )
        overlay_image_2 = Image_Manager.add_text(
            base=base,
            text=meme_text["party_two"],
            position=(800, 200),
            font_size=40,
            text_color="white",
            wrapped_width=12,
        )
        
        base = Image.alpha_composite(base, overlay_image_2)
        self.save_image(base, overlay_image, user_input)
