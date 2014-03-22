from flask import request

from models import Sentence

from framework.restapi.protocols import APIBlueprint

from framework.restapi.constants import API_STATUS_OK

api_bp = APIBlueprint('api', __name__, url_prefix='/api')

@api_bp.route('/')
def get_status():
    return api_bp.make_response(status=API_STATUS_OK)

@api_bp.route('/translations', methods=['GET'])
def get_translations():
    original_texts = [request.args['text']]
    found_sentences = Sentence.query.filter(Sentence.text.in_(original_texts))
    result_dicts = dict(
        (found_sentence.text,
         [translation.text for translation in found_sentence.translations])
        for found_sentence in found_sentences)

    return api_bp.make_response(status=API_STATUS_OK, result=result_dicts)
