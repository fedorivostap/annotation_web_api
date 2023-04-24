import flask.logging
from flask import Flask, request, render_template, redirect, url_for
import logging
import spacy
from spacy import displacy

nlp = spacy.load("en_core_web_sm")
app = Flask(__name__)


# configuring flask logging
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


@app.route("/train")
def train_model():
    return render_template("train.html")


@app.route("/annotate_test", methods=['GET', 'POST'])
def annotate():
    return render_template("annotate_test.html")


@app.route("/annotated", methods=["POST", "GET"])
def annotated():
    if request.method == "POST":
        text = request.form["text-for-annotation"]
        return text
    else:
        # for GET request
        return render_template("annotate.html")


@app.route('/submit', methods=['GET', 'POST'])
def submit():
    text = request.form['text']
    logger.info('Getting input text')
    # Annotating text
    doc = nlp(text)
    logger.info('Annotating text')
    html = displacy.render(doc, style="ent", page=True)
    return html


@app.route('/description', methods=['GET', 'POST'])
def description():
    return render_template("description.html")


if __name__ == '__main__':
    app.run(debug=True)
