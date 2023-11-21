# *_*coding:utf-8 *_*
# @Author : YueMengRui
from PIL import Image, ImageDraw, ImageFont


def create_font(txt, sz, font_path="static/simfang.ttf"):
    font_size = int(sz[1] * 0.99)
    font = ImageFont.truetype(font_path, font_size, encoding="utf-8")
    length = font.getlength(txt)
    if length > sz[0]:
        font_size = int(font_size * sz[0] / length)
        font = ImageFont.truetype(font_path, font_size, encoding="utf-8")
    return font


def draw_image(img_h, img_w, table):
    canvas = Image.new('RGB', (img_w, img_h), (255, 255, 255))
    draw = ImageDraw.Draw(canvas)

    for cell in table:
        draw.rectangle((cell.box[0] - 1, cell.box[1] - 1, cell.box[2] + 1, cell.box[3] + 1), outline=(0, 0, 0), width=2)

        font = create_font(cell.text, (cell.box[2] - cell.box[0] - 20, cell.box[3] - cell.box[1] - 20))
        draw.text((cell.box[0], cell.box[1]), cell.text, fill=(0, 0, 0), font=font)

    return canvas
