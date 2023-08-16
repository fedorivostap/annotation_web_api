from flask import Blueprint, request, render_template
from markupsafe import Markup
import spacy
from spacy import displacy
from spacy.language import Language
from spacy_crfsuite import CRFEntityExtractor, CRFExtractor
from bs4 import BeautifulSoup

text_annotation_blueprint = Blueprint('text_annotation', __name__)


@Language.factory("ner_crf")
def create_component(nlp, name):
    crf_extractor = CRFExtractor().from_disk("path_to_crf_model")
    return CRFEntityExtractor(nlp, crf_extractor=crf_extractor)


class TextAnnotator:
    def __init__(self):
        self.nlp = spacy.load("pl_core_news_sm")

    def annotate(self, text=None, model=None):
        if text is None or model is None:
            raise ValueError("You must provide text for annotation and specify the model you want to use!")

        if model == "standard":
            doc = self.nlp(text)
            html = Markup(displacy.render(doc, style="ent", page=True))
        else:
            self.nlp.disable_pipe("ner")
            self.nlp.add_pipe("ner_crf")
            doc = self.nlp(text)
            html = Markup(displacy.render(doc, style="ent", page=True))

        soup = BeautifulSoup(html, 'html.parser')
        html_body = ''.join(str(tag) for tag in soup.body.contents)
        html = html_body

        return html


@text_annotation_blueprint.route("/annotate", methods=['GET', 'POST'])
def annotate():
    if request.method == 'POST':
        text = request.form.get('text')
        model = request.form.get('model')

        if not text or not model:
            return render_template("annotate.html")

        annotator = TextAnnotator()
        html = annotator.annotate(text, model)
        return render_template("annotate.html", result=html)
    else:
        return render_template("annotate.html")
