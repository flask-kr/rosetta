import flask
import json


class APIResponseMaker(object):
    def make_response(self, models):
        return repr(self._marshal_models(models))

    @staticmethod
    def _marshal_models(models):
        response_dict = {}
        for model in models:
            response_dict.update(model.marshal())
        return response_dict


class JSONAPIResponseMaker(APIResponseMaker):
    RESPONSE_HEADERS = {
        'Content-Type': 'application/json; charset=utf-8'
    }

    def make_response(self, models):
        response_dict = self._marshal_models(models)
        response_text = json.dumps(response_dict)

        response = flask.make_response(response_text)
        response.headers.extend(self.RESPONSE_HEADERS)
        return response


class APIBlueprint(flask.Blueprint):
    API_RESPONSE_MAKER_DICT = {
        'json': JSONAPIResponseMaker()
    }

    def make_response(self, models):
        api_response_maker = self.API_RESPONSE_MAKER_DICT['json']
        return api_response_maker.make_response(models)

