from common.makememe.generator.prompts.prompt import Prompt
import datetime
from PIL import Image

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
        self.make_image(self.name, meme_text=meme_text, user_input=user_input)
        
