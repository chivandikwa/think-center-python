import uuid
import os

from typing import Tuple

from PIL import Image, ImageDraw
from colorgram import colorgram


class PaletteService:

    @staticmethod
    def get_image_with_palette(infile: str, outline_width: float, palette_length_div: float, outline_color,
                               num_colors: int = 12):
        colors = colorgram.extract(infile, 12)
        original_image: Image = Image.open(infile)
        width, height = original_image.size
        palette_height: int = int(height / palette_length_div)
        final_image: Image = Image.new(original_image.mode, (width, height + palette_height))
        palette: Image = Image.new(original_image.mode, (width, palette_height))
        draw_api: ImageDraw = ImageDraw.Draw(palette)
        pos_x: float = 0
        pos_x2: float = 0
        swatch_size: float = width / num_colors
        swatch_size2: int = 100

        for col in colors:
            draw_api.rectangle([pos_x, 0, pos_x + swatch_size, palette_height], fill=col.rgb, width=outline_width,
                               outline=outline_color)
            pos_x = pos_x + swatch_size
            pos_x2 = pos_x2 + swatch_size2

        del draw_api
        box: Tuple[int, float, float, float] = (0, height, width, height + palette_height)

        final_image.paste(original_image)
        final_image.paste(palette, box)

        file_name = f"{str(uuid.uuid4())}.jpg"
        file_path = os.path.join(os.path.dirname(__file__), file_name)
        final_image.save(file_path, 'jpeg', quality=100, optimize=True)
        return file_path
