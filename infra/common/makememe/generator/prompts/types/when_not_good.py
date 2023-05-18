
from PIL import Image
from common.makememe.generator.design.image_manager import Image_Manager
from common.makememe.generator.prompts.prompt import Prompt

class When_Not_Good(Prompt):
    id = 16
    name = "When_Not_Good"
    description = "when something is really bad"

    def __init__(self):
        self.instruction = """
###
Message:When all your friends are getting married and you've not been on a date.
Meme:{"subject": "When all your friends are getting married and you've not been on a date."}
###
Message:I got a 4 year engineering degree and now can't remember calculus.
Meme:{"subject": "When you get a 4 year engineering degree and now can't remember calculus."}
###
Message:It's not good that this new strain is spreading fast
Meme:{"subject": "When the new strain is spreading fast"}
###
Message:When I have to run a full marathon, but I haven't trained for it.
Meme:{"subject": "When I have to run a full marathon, but I haven't trained for it."}
###
"""

    def create(self, meme_text, user_input):
        base = self.make_image(meme_text, user_input)

        overlay_image = Image_Manager.add_text(
            base=base,
            text=meme_text["subject"],
            position=(100, 50),
            font_size=45,
            wrapped_width=40,
        )

        return self.save_image(base, overlay_image, user_input)
