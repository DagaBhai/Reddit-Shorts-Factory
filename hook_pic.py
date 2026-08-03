from PIL import Image, ImageDraw, ImageFont
import os


def wrap_text(draw, text, font, max_width):
    """Wrap text so each line fits within max_width pixels."""
    words = text.split()
    lines = []
    current_line = ""

    for word in words:
        test_line = word if current_line == "" else current_line + " " + word
        if draw.textlength(test_line, font=font) <= max_width:
            current_line = test_line
        else:
            lines.append(current_line)
            current_line = word

    if current_line:
        lines.append(current_line)

    return "\n".join(lines)


def create_rectangle_with_overlays(text):

    width, height = 800, 400
    bg_color = (255, 255, 255, 255)
    corner_radius = 40

    canvas = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    mask = Image.new("L", (width, height), 0)

    mask_draw = ImageDraw.Draw(mask)
    mask_draw.rounded_rectangle(
        [(0, 0), (width, height)],
        radius=corner_radius,
        fill=255
    )

    base = Image.new("RGBA", (width, height), bg_color)
    canvas.paste(base, (0, 0), mask)

    try:
        overlay_img = Image.open("logo.png").convert("RGBA")
    except FileNotFoundError:
        print("logo.png not found. Using dummy image.")
        overlay_img = Image.new("RGBA", (150, 150), (231, 76, 60, 255))

    overlay_img = overlay_img.resize((150, 150))

    logo_x = (width - overlay_img.width) // 2
    logo_y = 10

    canvas.paste(overlay_img, (logo_x, logo_y), overlay_img)

    draw = ImageDraw.Draw(canvas)

    try:
        font = ImageFont.truetype(
            r"C:\Windows\Fonts\arialbd.ttf",
            36
        )
    except:
        font = ImageFont.load_default()

    horizontal_padding = 40
    max_text_width = width - 2 * horizontal_padding

    wrapped_text = wrap_text(
        draw,
        text,
        font,
        max_text_width
    )

    bbox = draw.multiline_textbbox(
        (0, 0),
        wrapped_text,
        font=font,
        spacing=8,
        align="center"
    )

    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]

    text_area_top = 170
    text_area_height = height - text_area_top

    text_x = (width - text_width) // 2
    text_y = text_area_top + (text_area_height - text_height) // 2

    draw.multiline_text(
        (text_x, text_y),
        wrapped_text,
        font=font,
        fill="black",
        align="center",
        spacing=8,
    )

    canvas.save("final_output.png")
    canvas.show()


if __name__ == "__main__":
    create_rectangle_with_overlays(
        "I found a hidden room in my new apartment but the walls were entirely covered in my own childhood photos."
    )