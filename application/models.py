# -*- coding:utf8 -*-
from framework import db
from datetime import datetime


class User(db.Model):
    """
    사용자
    """

    id = db.Column(db.Integer, primary_key=True)
    uid = db.Column(db.String(128), unique=True)
    
    name = db.Column(db.String(64))

    ctime = db.Column(db.DateTime, default=datetime.now(), nullable=False)
    mtime = db.Column(db.DateTime, default=datetime.now(), nullable=False)

    def __repr__(self):
        return '%s(id=%s, uid="%s", name="%s")' % (self.__class__.__name__, self.id, self.uid, self.name)


class Site(db.Model):
    """
    사이트
    """

    id = db.Column(db.Integer, primary_key=True)

    url = db.Column(db.String(32), unique=True)

    ctime = db.Column(db.DateTime, default=datetime.now(), nullable=False)
    mtime = db.Column(db.DateTime, default=datetime.now(), nullable=False)


class Page(db.Model):
    """
    페이지
    """

    id = db.Column(db.Integer, primary_key=True)
    site_id = db.Column(db.Integer, db.ForeignKey(Site.id))

    path = db.Column(db.String(80), unique=True)

    ctime = db.Column(db.DateTime, default=datetime.now(), nullable=False)
    mtime = db.Column(db.DateTime, default=datetime.now(), nullable=False)


class Sentence(db.Model):
    """
    문장
    """

    id = db.Column(db.Integer, primary_key=True)
    site_id = db.Column(db.Integer, db.ForeignKey(Site.id))
    page_id = db.Column(db.Integer, db.ForeignKey(Page.id))
    
    text = db.Column(db.String(32))

    ctime = db.Column(db.DateTime, default=datetime.now(), nullable=False)
    mtime = db.Column(db.DateTime, default=datetime.now(), nullable=False)


class UserTranslation(db.Model):
    """
    사용자 번역 
    """

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey(User.id))
    sentence_id = db.Column(db.Integer, db.ForeignKey(Sentence.id))

    text = db.Column(db.String(32))

    ctime = db.Column(db.DateTime, default=datetime.now(), nullable=False)
    mtime = db.Column(db.DateTime, default=datetime.now(), nullable=False)


class UserSelection(db.Model):
    """
    사용자 선택
    """

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey(User.id))
    sentence_id = db.Column(db.Integer, db.ForeignKey(Sentence.id))
    user_translation_id = db.Column(db.Integer, db.ForeignKey(UserTranslation.id))

    ctime = db.Column(db.DateTime, default=datetime.now(), nullable=False)
    mtime = db.Column(db.DateTime, default=datetime.now(), nullable=False)


if __name__ == '__main__':
    user = User(uid='jaru', name='Song Young-Jin')
    print user
