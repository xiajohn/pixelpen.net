import traceback
from PIL import Image, ImageDraw, ImageFont, ImageOps, ImageChops
# from makememe.generator.design.font import font_path
from common.makememe.generator.prompts.helper import Helper
import os

class Image_Manager:
    def __init__(self):
        print("Image manager create")

    @staticmethod
    def add_text(
        base,
        text,
        position,
        font_size,
        text_color="black",
        text_width_proportion=4,
        wrapped_width=None,
        rotate_degrees=None,
    ):
        try:
            overlay_image = Image.new("RGBA", base.size, (0, 0, 0, 0))
            if wrapped_width is not None:
                text = Helper.wrap(text, wrapped_width)

            current_path = os.path.dirname(os.path.abspath(__file__))
            font_path = os.path.join(current_path, "impact.ttf")
            font = ImageFont.truetype(font_path, font_size)
            draw = ImageDraw.Draw(overlay_image)
            fill = (0, 0, 0, 255)
            if text_color == "white":
                fill = (255, 255, 255, 255)
            draw.text(position, text, font=font, fill=fill)
            if rotate_degrees is not None:
                overlay_image = overlay_image.rotate(rotate_degrees)

            return overlay_image
        except Exception as e:
            print(f"Error occurred in add_text: {e}")
            traceback.print_exc()  # Print full exception stack trace
            raise  # Reraise the exception

