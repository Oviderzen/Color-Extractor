from flask import Flask, render_template, request
from flask_bootstrap import Bootstrap
from werkzeug.utils import secure_filename
from colorthief import ColorThief
import os


##### This is for testing purposes only. Should use environment variable instead.
SECRET_KEY = 'top_secret'

app = Flask(__name__)
app.config['SECRET_KEY'] = SECRET_KEY
app.config['UPLOAD_FOLDER'] = "Uploaded-Images"
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
app.config['MAX_CONTENT_LENGTH'] = 30 * 1000 * 1000
Bootstrap(app)


@app.route('/', methods=["GET", "POST"])
def home():
    return render_template('index.html')


@app.route('/palette', methods=["GET", "POST"])
def extract_color():
    image = request.files['file']
    filename = secure_filename(image.filename)
    save_folder = os.path.join(app.static_folder, 'Uploaded-Images')
    os.makedirs(save_folder, exist_ok=True)
    image.save(os.path.join(save_folder, filename))
    image_path = os.path.join('static/Uploaded-Images', filename)
    color_thief = ColorThief(os.path.join(save_folder, filename))
    image_colors = color_thief.get_palette(color_count=11, quality=1)
    return render_template('palette.html', image_path=image_path, image_colors=image_colors)


if __name__ == '__main__':
    app.run(debug=True)