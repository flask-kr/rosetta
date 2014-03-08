from framework.restapi.protocols import APIBlueprint

from framework.restapi.constants import API_STATUS_OK

api = APIBlueprint('api', __name__, url_prefix='/api')

@api.route('/')
def get_status():
    return api.make_response([API_STATUS_OK])