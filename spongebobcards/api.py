from flask import Blueprint, jsonify, request, send_file
from io import BytesIO
from PIL import Image, ImageDraw, ImageFont
from functools import wraps

# Set up api Blueprint
api = Blueprint('api', __name__)

@api.route("/create", methods=['GET'])
def create():
    #
    #  Get all the parameters
    #
    background_image = "spongebobcards/static/backgrounds/" + request.args.get('background') + ".jpg"
    top_text = request.args.get('top_text')
    bottom_text = request.args.get('bottom_text')
    font_color = request.args.get('font_color')
    should_outline = False if (request.args.get('should_outline')) == "False" else True
    outline_color = request.args.get('outline_color')

    #
    #  Convert HEX to RGB tuple
    #
    if should_outline:
        outline_color_rgb = tuple(int(outline_color[i:i+2], 16) for i in (0, 2 ,4))
    font_color_rgb = tuple(int(font_color[i:i+2], 16) for i in (0, 2 ,4))

    #
    #  Create image and determine appropriate font size
    #
    font_size = 1
    fraction_of_image = 0.7
    font_dir = "spongebobcards/static/sometimelater/Some Time Later.otf"

    image = Image.open(background_image)
    draw = ImageDraw.Draw(image)
    font = ImageFont.truetype(font_dir, font_size)

    if font.getsize(top_text)[0] > font.getsize(bottom_text)[0]:
        while font.getsize(top_text)[0] < fraction_of_image*image.size[0] and font_size <= 120:
            font_size += 1
            font = ImageFont.truetype(font_dir, font_size)
    elif font.getsize(top_text)[0] < font.getsize(bottom_text)[0]:
        while font.getsize(bottom_text)[0] < fraction_of_image*image.size[0] and font_size <= 120:
            font_size += 1
            font = ImageFont.truetype(font_dir, font_size)
    else:
        while font.getsize(top_text)[0] < fraction_of_image*image.size[0] and font_size <= 120:
            font_size += 1
            font = ImageFont.truetype(font_dir, font_size)

    #
    #  Draw text on image
    #
    imageWidth, imageHeight = image.size

    topTextWidth, topTextHeight = draw.textsize(top_text, font=font)
    bottomTextWidth, bottomTextHeight = draw.textsize(bottom_text, font=font)

    topTextCoordinates = ((imageWidth-topTextWidth)/2,((imageHeight-topTextHeight)/2)-(topTextHeight/2))
    bottomTextCoordinates = ((imageWidth-bottomTextWidth)/2,((imageHeight-bottomTextHeight)/2)+(bottomTextHeight/2))

    #
    #  Draw outline if requested
    #
    if should_outline:
        draw.text((topTextCoordinates[0]-3, topTextCoordinates[1]-3), top_text, outline_color_rgb, font=font)
        draw.text((topTextCoordinates[0]+3, topTextCoordinates[1]-3), top_text, outline_color_rgb, font=font)
        draw.text((topTextCoordinates[0]-3, topTextCoordinates[1]+3), top_text, outline_color_rgb, font=font)
        draw.text((topTextCoordinates[0]+3, topTextCoordinates[1]+3), top_text, outline_color_rgb, font=font)

        draw.text((bottomTextCoordinates[0]-3, bottomTextCoordinates[1]-3), bottom_text, outline_color_rgb, font=font)
        draw.text((bottomTextCoordinates[0]+3, bottomTextCoordinates[1]-3), bottom_text, outline_color_rgb, font=font)
        draw.text((bottomTextCoordinates[0]-3, bottomTextCoordinates[1]+3), bottom_text, outline_color_rgb, font=font)
        draw.text((bottomTextCoordinates[0]+3, bottomTextCoordinates[1]+3), bottom_text, outline_color_rgb, font=font)


    draw.text(topTextCoordinates, top_text, font_color_rgb, font=font)
    draw.text(bottomTextCoordinates, bottom_text, font_color_rgb, font=font)

    byte_io = BytesIO()
    image.save(byte_io, 'JPEG')
    byte_io.seek(0)
    image.close()

    return send_file(byte_io, mimetype='image/jpeg')
