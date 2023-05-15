from common.makememe.generator.prompts.prompt import Prompt
import datetime
from PIL import Image
from common.makememe.generator.design.image_manager import Image_Manager


class Sad(Prompt):
    id = 1
    name = "Sad"
    description = "sad"

    def __init__(self):
        self.instruction = """
###
Message:We still haven't been to Mars and it makes me cry
Meme:{"sad_part": "We still haven't been to Mars"}
###
Message:My college degree didn't get me a job and now I am in debt
Meme:{"sad_part": "Your college degree didn't get you a job and now you're in debt"}
###
Message:I have to actually read to learn something
Meme:{"sad_part": "You have to actually read to learn something"}
###
Message:I can't run a marathon, but I wish I could
Meme:{"sad_part": "You can't run a marathon"}
###
Message:I am as tall as i will ever be and I guess it is too bad
Meme:{"sad_part": "You are as tall as you will ever be"}
###
Message:It is such a bummer that dogs don't live as long as people
Meme:{"sad_part": "Dogs don't live as long as people"}
###
Message:I may never be able to go to the moon and it makes me sad
Meme:{"sad_part": "You may never be able to go to the moon"}
###
Message:Finding a swe internship is challenging.
Meme:{"sad_part": "You may never find a SWE internship"}
###
Message:Happy
Meme:{"sad_part": "it doesn't matter if we're happy"}
###
"""

    def create(self, meme_text, user_input):
        self.make_image(self.name, meme_text=meme_text, user_input=user_input)
        