from PIL import Image, ImageDraw, ImageFont
from random import sample

def generate(string,color_bg=False):
    colors = [(0, 0, 0), (255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 0), (0, 255, 255), (255, 0, 255), (192, 192, 192), (128, 128, 128), (128, 0, 0), (128, 128, 0), (0, 128, 0), (128, 0, 128), (0, 128, 128), (0, 0, 128)]
    if color_bg:
        bg = color_bg
    else:
        bg = sample(colors, 1)[0]
    try:
        img = Image.new('RGB', (300, 300), color=bg)
    except:
        print("Invalid color")
        print("Color has been randomly selected")
        bg = sample(colors, 1)[0]
        img = Image.new('RGB', (300, 300), color=bg)
    width, height = img.size
    draw = ImageDraw.Draw(img)
    font = ImageFont.truetype('arial.ttf', size=height)
    text = string.upper()
    color = 'rgb(255, 255, 255)'
    draw.text((width/2, height/2), text[0], fill=color, font=font, anchor='mm')
    return img



