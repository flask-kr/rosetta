# -*- coding:utf8 -*-
import pytest

from application import db
from application import app_factory

from application.models import *

@pytest.fixture(scope="module")
def __create_app():
    return app_factory.create_app(
        "$PROJECT_DIR/etc/configs/default_config.yml",
        code_config_dict={
            'SQLALCHEMY_ECHO': False,
        })


def test_translation():
    __create_app()

    user1 = User(uid='u0001', name='jaru')
    site1 = Site(url='http://site.com')
    page1 = Page(path='/page', site_id=site1.id)

    sentence1 = Sentence(
        site_id=site1.id, page_id=page1.id, text=u"test")

    user_translation1 = UserTranslation(
        user_id=user1.id, sentence_id=sentence1.id, text=u"테스트")

    user_selection1 = UserSelection(
        user_id=user1.id,
        sentence_id=sentence1.id,
        user_translation_id=user_translation1.id
    )

    db.session.add(user1)
    db.session.add(site1)
    db.session.add(page1)
    db.session.add(sentence1)
    db.session.add(user_translation1)
    db.session.add(user_selection1)
    db.session.commit()

if __name__ == '__main__':
    test_users()