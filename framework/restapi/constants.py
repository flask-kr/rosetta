from enum import IntEnum

from gettext import gettext as _


class APIStatusCode(IntEnum):
    OK = 0


class APIStatus(object):
    def __init__(self, code, memo):
        self.code = code
        self.memo = memo

    def marshal(self):
        return {
            'status': {
                'code': int(self.code),
                'memo': self.memo,
            }
        }


API_STATUS_OK = APIStatus(code=APIStatusCode.OK, memo=_('API_STATUS_OK'))
