from framework.restapi.protocols import APIBlueprint

from framework.restapi.constants import API_STATUS_OK

api_bp = APIBlueprint('api', __name__, url_prefix='/api')

@api_bp.route('/')
def get_status():
    return api_bp.make_response([API_STATUS_OK])
