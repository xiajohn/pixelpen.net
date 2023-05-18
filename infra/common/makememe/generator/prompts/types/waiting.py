
from PIL import Image
from common.makememe.generator.design.image_manager import Image_Manager
from common.makememe.generator.prompts.prompt import Prompt

class Waiting(Prompt):
    id =3
    name = "Waiting"
    description = "waiting"

    def __init__(self):
        self.instruction = """
###
Message:I've been waiting for SpaceX to launch the starship for ever
Meme:{"subject": "SpaceX Startship"}
###
Message:I can't wait for makememe.ai to launch, but it's taking a little while
Meme:{"subject": "makememe.ai"}
###
Message:Drakes new album is going to be fire. Why do I have to wait
Meme:{"subject": "Drakes new album"}
###
Message:I want to create an NFT, but opensea.com is taking a while to load
Meme:{"subject": "opensea.com"}
###
"""

    def create(self, meme_text, user_input):
        base = self.make_image(meme_text, user_input)

        overlay_image = Image_Manager.add_text(
            base=base,
            text=meme_text["subject"],
            position=(600, 950),
            font_size=40,
            wrapped_width=20,
        )
        
        return self.save_image(base, overlay_image, user_input)