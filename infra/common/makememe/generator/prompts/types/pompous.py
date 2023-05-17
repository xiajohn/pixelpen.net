from common.makememe.generator.prompts.prompt import Prompt
import datetime
from PIL import Image
from common.makememe.generator.design.image_manager import Image_Manager


class Pompous(Prompt):
    id = 5
    name = "Pompous"
    description = "pompous"

    def __init__(self):
        self.instruction = """
###
Message:People who run marathon think they are superior. Maybe that's the case
Meme:{"subject":"Running marathon"}
###
Message:People who play chess seem to think they are better than people who play checkers
Meme:{"subject":"People who play chess"}
###
Message:Coding gives people a feeling of being great
Meme:{"subject":"Coding"}
###
Message:Shareholders that don't have to report to any managers and make money think it is great.
Meme:{"subject":"Not reporting to any managers"}
###
Message:Being able to do a front flip makes people pompus
Meme:{"subject":"Being able to do a front flip"}
###
Message:That was fun, but now I need to learn how to ride a bicycle
Meme:{"subject":"Riding sa bicycle"}
###
Message:Using a drip coffee system works, but have you tried using a french press??
Meme:{"subject":"using a french press"}
###
"""

    def create(self, meme_text, user_input):
        base = self.make_image(meme_text, user_input)

        overlay_image = Image_Manager.add_text(
            base=base,
            text=meme_text["subject"],
            position=(30, 900),
            font_size=40,
            wrapped_width=10,
        )

        
        return self.save_image(base, overlay_image, user_input)
