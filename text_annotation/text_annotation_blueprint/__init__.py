from flask import Blueprint

text_annotation_blueprint = Blueprint('text_annotation', __name__, template_folder="/templates")

from text_annotation.text_annotation_blueprint.views import *