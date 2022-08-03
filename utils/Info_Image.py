from PIL import Image, ImageDraw, ImageFont

FONT = ImageFont.truetype("utils/fonts/Comfortaa-Regular.ttf", 40)
FONT_H = ImageFont.truetype("utils/fonts/Comfortaa-Regular.ttf", 80)


def render_information(color: tuple = (0, 0, 255), **kwargs):
    img = Image.open("Bat.jpg")
    write = ImageDraw.Draw(img)
    heading = ImageDraw.Draw(img)
    w, h = img.size
    heading.text(
        (w // 2, h // 8), "ALFRED", fill=(255, 255, 255), anchor="mm", font=FONT_H
    )

    count = 0
    text = ""
    for i, j in kwargs.items():
        count += h // len(kwargs)
        text += f"{i.upper()} -> {j}\n"
    text = text.replace("_", " ")
    write.text((0, 10), text=text, font=FONT, fill=color, align="left", spacing=5.4)
    img.save("BotInfo.jpg")
