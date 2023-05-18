
from PIL import Image
from common.makememe.generator.design.image_manager import Image_Manager
from common.makememe.generator.prompts.prompt import Prompt

class Is_Better(Prompt):
    id = 6
    name = "Is_Better"
    description = "this is better than that"

    def __init__(self):
        self.instruction = """
###
Message:I like coffee, but tea is much better
Meme:{"worse":"coffee", "better":"tea"}
###
Message:Dr. Dre is nothing compared to Kanye
Meme:{"worse":"Dr. Dre", "better":"Kanye"}
###
Message:I don't want a Honda, I want a Tesla
Meme:{"worse":"Honda", "better":"Tesla"}
###
Message:We don't need a new car, we need a new robot
Meme:{"worse":"new car", "better":"new robot"}
###
Message:Facebook is no good compared to Twitter
Meme:{"worse":"Facebook", "better":"Twitter"}
###
Message:Dogs make you happy while cats make you sad
Meme:{"worse":"cats", "better":"dogs"}
###
Message:I love apples, while I don't care so much for oranges
Meme:{"worse":"oranges","better":"apples"}
###
Message:Daft punk is the greatest, while U2 is not that good
Meme:{"worse":"u2","better":"daft punk"}
###
Message:Riding a bike on dirt is more fun than writing a bike on the street
Meme:{"worse":"writing a bike on the street","better":"riding a bike on dirt"}
###
Message:Surfing in warm water is more enjoyable than surfing in cold water
Meme:{"worse":"surfing in cold water","better":"surfing in warm water"}
###
Message:Spending time on the internet to make people laugh is better then doing it to cause outrage
Meme:{"worse":"Spending time on the internet to cause outrage","better":"Spending time on the internet to making people laugh"}
###
Message:Humans making memes ok, AI making memes awesome.
Meme:{"worse":"human making memes","better":"AI making memes"}
###
Message:better
Meme:{"worse":"better","better":"better 2.0"}
###
"""

    def create(self, meme_text, user_input):
        base = self.make_image(meme_text, user_input)

        overlay_image = Image_Manager.add_text(
            base=base,
            text=meme_text["worse"],
            position=(625, 100),
            font_size=50,
            wrapped_width=15,
        )
        overlay_image_2 = Image_Manager.add_text(
            base=base,
            text=meme_text["better"],
            position=(625, 525),
            font_size=50,
            wrapped_width=15,
        )
        
        base = Image.alpha_composite(base, overlay_image_2)
        return self.save_image(base, overlay_image, user_input)
