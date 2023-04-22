from flask import Flask, request, render_template, redirect, url_for
import spacy
from spacy import displacy

nlp = spacy.load("en_core_web_sm")
app = Flask(__name__)


@app.route('/')
def home():
    return render_template("index.html")


@app.route("/annotated", methods=["POST", "GET"])
def annotated():
    if request.method == "POST":
        text = request.form["text-for-annotation"]
        return text
    else:
        # for GET request
        return render_template("annotated.html")


@app.route('/submit', methods=['POST'])
def submit():
    name = request.form.get('name')
    # Do something with the name
    doc = nlp(name)
    html = displacy.render(doc, style="ent", page=True)
    return html


if __name__ == '__main__':
    app.run()
