from common.makememe.generator.prompts.prompt import Prompt
import datetime
from PIL import Image
from common.makememe.generator.design.image_manager import Image_Manager


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

    def create(self, meme_text):
        with Image.open(f"makememe/static/meme_pics/{self.name.lower()}.jpg").convert(
            "RGBA"
        ) as base:

            overlay_image = Image_Manager.add_text(
                base=base,
                text=meme_text["subject"],
                position=(600, 950),
                font_size=40,
                wrapped_width=20,
            )
            watermark = Image_Manager.add_text(
                base=base, text="makememe.ai", position=(30, 1100), font_size=20
            )

            base = Image.alpha_composite(base, watermark)
            out = Image.alpha_composite(base, overlay_image)
            if out.mode in ("RGBA", "P"):
                out = out.convert("RGB")
                # User.objects.filter()
                date = datetime.datetime.now()
                image_name = f"{date}.jpg"
                file_location = f"makememe/static/creations/{image_name}"
                out.save(file_location)
                return image_name
