from flask import Flask, render_template, request, redirect, send_file, url_for
from os import listdir
from os.path import isfile, join
from .api import api
import re, requests

# Create Flask app
app = Flask(__name__)

# Register Blueprints
app.register_blueprint(api, url_prefix='/api')

def tryint(s):
    try:
        return int(s)
    except:
        return s

def alphanum_key(s):
    return [tryint(c) for c in re.split('([0-9]+)', s)]

# Load Index page
@app.route('/')
def index():
    THUMB_DIR = "spongebobcards/static/backgrounds/thumbnails/"
    files = [f for f in listdir(THUMB_DIR) if isfile(join(THUMB_DIR, f))]
    files.sort(key=alphanum_key)
    return render_template("index.html", files=files, error=request.args.get('error'))

@app.route('/image', methods=['GET', 'POST'])
def image():
    try:
        top_text = request.form.get("topText").strip()
        bottom_text = request.form.get("bottomText").strip()
        font_color = request.form.get("fontColor").strip()
        background = request.form.get("background").split(".")[0].strip()
    except:
        return redirect(url_for('index', error="You did not complete all the options."))

    if not top_text or not bottom_text or not font_color or not background:
        return redirect(url_for('index', error="You did not complete all the options."))

    try:
        request.form.get("outlineCheckbox").strip()
        outline_color = request.form.get("outlineColor").strip()
        should_outline = True
    except:
        should_outline = False
        outline_color = None

    return render_template("image.html", top_text=top_text, bottom_text=bottom_text, background=background, font_color=font_color, should_outline=should_outline, outline_color=outline_color)

@app.route('/about')
def about():
    return render_template("about.html")

@app.route('/docs')
def docs():
    return render_template("api.html")
