from common.makememe.generator.prompts.prompt import Prompt
import datetime
from PIL import Image
from common.makememe.generator.prompts.helper import Helper
from common.makememe.generator.design.image_manager import Image_Manager


class Equal(Prompt):
    id = 12
    name = "Equal"
    description = "something is the same as something else"

    def __init__(self):
        self.instruction = """
###
Message:Tea and coffee are equally is good. They both make me happy
Meme:{"first":"Tea", "second":"coffee"}
###
Message:Both Dr. Dre and Kanye are amazing. I love them both
Meme:{"first":"Dr. Dre", "second":"Kanye"}
###
Message:If I had to decide between Honda and Tesla I couldn't. They are both great.
Meme:{"first":"Honda", "second":"Tesla"}
###
Message:Riding a bike on dirt is just as fun as riding on the street
Meme:{"first":"writing a bike on the dirt","second":"writing a bike on the street"}
###
Message:Surfing in warm water is the same as surfing in cold water. They are equally fun
Meme:{"first":"surfing in cold water","second":"surfing in warm water"}
###
Message:alsdjkfa
Meme:{"first":"alsdjkfa","second":"alsdjkfa"}
###
"""

    def create(self, meme_text, user_input):

        base = self.make_image(meme_text, user_input)

        overlay_image = Image_Manager.add_text(
            base=base,
            text=meme_text["first"],
            position=(70, 180),
            font_size=45,
            wrapped_width=12,
            rotate_degrees=345,
        )
        overlay_image_2 = Image_Manager.add_text(
            base=base,
            text=meme_text["second"],
            position=(575, 100),
            font_size=45,
            wrapped_width=12,
            rotate_degrees=345,
        )
        
        base = Image.alpha_composite(base, overlay_image)
        return self.save_image(base, overlay_image_2, user_input)
