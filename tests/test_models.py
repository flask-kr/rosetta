# -*- coding:utf8 -*-
import pytest

from framework import db
from application import app_factory

from application.models import *

CODE_CONFIG_DICT = {
    'SQLALCHEMY_ECHO': False,
}

@pytest.fixture(scope="module")
def __create_application():
    return app_factory.create_application(
        "$PROJECT_DIR/etc/configs/default_config.yml",
        custom_config_dict=CODE_CONFIG_DICT)


def test_translation():
    __create_application()

    db.create_all()

    user1 = User(uid='u0001', name='jaru')
    site1 = Site(url='http://site.com')
    page1 = Page(path='/page', site=site1)

    sentence1 = Sentence(
        page=page1, text=u"test")

    translation1 = Translation(
        user=user1, sentence=sentence1, text=u"테스트")

    selection1 = Selection(
        user=user1,
        sentence=sentence1,
        translation=translation1
    )

    db.session.add(user1)
    db.session.add(site1)
    db.session.add(page1)
    db.session.add(sentence1)
    db.session.add(translation1)
    db.session.add(selection1)
    db.session.commit()

    site2 = Site.query.filter(Site.url == 'http://site.com').one()
    assert(site2.pages.count() == 1)

    page2 = site2.pages.filter(Page.path == '/page').one()
    user2 = User.query.filter(User.uid == 'u0001').one()

    contents2 = [
        (sentence.text, translation.text)
        for selection, sentence, translation in Selection
        .join_sentence_and_translation_for_page_and_user(
            page=page2, user=user2)
        .all()]

    assert(len(contents2) == 1)
    assert(contents2[0] == (u"test", u"테스트"))



if __name__ == '__main__':
    CODE_CONFIG_DICT = {
        'SQLALCHEMY_ECHO': True,
        }
    test_translation()