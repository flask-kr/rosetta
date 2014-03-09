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

    selections = db.relationship(lambda: Selection,
                                 backref='user', lazy='dynamic')

    translations = db.relationship(lambda: Translation,
                                   backref='user', lazy='dynamic')

    def __repr__(self):
        return '%s(id=%s, uid=%s, name=%s)' % \
               (self.__class__.__name__,
                self.id, repr(self.uid), repr(self.name))


class Site(db.Model):
    """
    사이트
    """

    id = db.Column(db.Integer, primary_key=True)

    url = db.Column(db.String(32), unique=True)

    ctime = db.Column(db.DateTime, default=datetime.now(), nullable=False)
    mtime = db.Column(db.DateTime, default=datetime.now(), nullable=False)

    pages = db.relationship(lambda: Page, backref='site', lazy='dynamic')

    def __repr__(self):
        return '%s(id=%s, url=%s)' % \
               (self.__class__.__name__, self.id, repr(self.url))


class Page(db.Model):
    """
    페이지
    """

    id = db.Column(db.Integer, primary_key=True)
    site_id = db.Column(db.Integer, db.ForeignKey(Site.id))

    path = db.Column(db.String(80), unique=True)

    ctime = db.Column(db.DateTime, default=datetime.now(), nullable=False)
    mtime = db.Column(db.DateTime, default=datetime.now(), nullable=False)

    sentences = db.relationship(lambda: Sentence,
                                backref='page', lazy='dynamic')


    def __repr__(self):
        return '%s(id=%s, path=%s, site=%s)' % \
               (self.__class__.__name__,
                self.id, repr(self.path), repr(self.site))


class Sentence(db.Model):
    """
    문장
    """

    id = db.Column(db.Integer, primary_key=True)
    page_id = db.Column(db.Integer, db.ForeignKey(Page.id))
    
    text = db.Column(db.String(32))

    ctime = db.Column(db.DateTime, default=datetime.now(), nullable=False)
    mtime = db.Column(db.DateTime, default=datetime.now(), nullable=False)

    translations = db.relationship(lambda: Translation,
                                   backref='sentence', lazy='dynamic')

    selections = db.relationship(lambda: Selection,
                                 backref='sentence', lazy='dynamic')

    def __repr__(self):
        return '%s(id=%s, text=%s, page=%s)' % \
               (self.__class__.__name__,
                self.id,
                repr(self.text),
                repr(self.page))


class Translation(db.Model):
    """
    사용자 번역 
    """

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey(User.id))
    sentence_id = db.Column(db.Integer, db.ForeignKey(Sentence.id))

    text = db.Column(db.String(32))

    ctime = db.Column(db.DateTime, default=datetime.now(), nullable=False)
    mtime = db.Column(db.DateTime, default=datetime.now(), nullable=False)

    selections = db.relationship(lambda: Selection,
                                 backref='translation', lazy='dynamic')

    def __repr__(self):
        return '%s(id=%s, text=%s, user=%s, sentence=%s)' % \
               (self.__class__.__name__,
                self.id,
                repr(self.text),
                repr(self.user),
                repr(self.sentence))


class Selection(db.Model):
    """
    사용자 선택
    """

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey(User.id))
    sentence_id = db.Column(db.Integer, db.ForeignKey(Sentence.id))
    translation_id = db.Column(db.Integer, db.ForeignKey(Translation.id))

    ctime = db.Column(db.DateTime, default=datetime.now(), nullable=False)
    mtime = db.Column(db.DateTime, default=datetime.now(), nullable=False)

    def __repr__(self):
        return '%s(id=%s, user=%s, sentence=%s, translation=%s)' % \
               (self.__class__.__name__,
                self.id,
                repr(self.user),
                repr(self.sentence),
                repr(self.translation))

    @classmethod
    def join_sentence_and_translation_for_page_and_user(cls, page, user):
        return db.session.query(cls, Sentence, Translation)\
            .filter(Sentence.page_id == page.id) \
            .filter(cls.user_id == user.id) \
            .filter(cls.sentence_id == Sentence.id)\
            .filter(cls.translation_id == Translation.id)

if __name__ == '__main__':
    def main():
        user = User(uid='jaru', name='Song Young-Jin')
        print user

    main()
