
from flask import Flask, render_template, send_from_directory
import os

app = Flask(__name__)

IMAGE_FOLDER = os.path.expanduser("~{os.sep}")



@app.route(f'/uploads/display_image.png')
def uploaded_file(filename='display_image.png'):
    return send_from_directory(IMAGE_FOLDER, filename)


@app.route('/')
def index():
    return render_template('index.html')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=4000, debug=True, threaded=True)
