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
        self.make_image(self.name, meme_text=meme_text, user_input=user_input)
        
