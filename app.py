from flask import Flask, request, render_template, redirect, url_for
from text_annotation.text_annotation_blueprint.views import text_annotation_blueprint
import logging

app = Flask(__name__)
app.register_blueprint(text_annotation_blueprint)


logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

file_handler = logging.FileHandler('app.log')
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

stream_handler = logging.StreamHandler()
stream_handler.setFormatter(formatter)
logger.addHandler(stream_handler)


@app.route('/')
def home():
    return render_template("index.html")


@app.route('/description', methods=['GET', 'POST'])
def description():
    return render_template("description.html")


if __name__ == '__main__':
    app.run(debug=True)
