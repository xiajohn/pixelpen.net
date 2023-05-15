from common.makememe.generator.prompts.prompt import Prompt
import datetime
from PIL import Image
from common.makememe.generator.design.image_manager import Image_Manager


class Change_My_Mind(Prompt):
    id = 10
    name = "Change_My_Mind"
    description = "This is the way it is in my opinion"

    def __init__(self):
        self.instruction = """
###
Message:Chocolate chip cookies are the best cookies. Try to change my mind.
Meme:{"opinion":" Chocolate chip cookies are the best cookies."}
###
Message:Learning to code is one of the most rewarding experiences. Change my mind.
Meme:{"opinion":"Learning to code is one of the most rewarding experiences."}
###
Message:Daft Punk is the greatest electronic band to ever exist and you can't convince me otherwise.
Meme:{"opinion":"Daft Punk is the greatest electronic band to ever exist. "}
###
Message:In my opinion, the best way to get a good grade in school is to study hard.
Meme:{"opinion":"The best way to get a good grade in school is to study hard. "}
###
"""

    def create(self, meme_text, user_input):
        self.make_image(self.name, meme_text=meme_text, user_input=user_input)