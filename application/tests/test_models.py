import pytest

from application import db
from application import app_factory

from application.models import *

@pytest.fixture(scope="module")
def __create_app():
    return app_factory.create_app("$PWD/etc/configs/default_config.yml")


def test_users():
    __create_app()

    u1 = User(uid='u0001', name='jaru')
    db.session.add(u1)
    db.session.commit()

if __name__ == '__main__':
    test_users()