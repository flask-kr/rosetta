# -*- coding:utf8 -*-
import re

from flask_sqlalchemy import SQLAlchemy
from flask_sqlalchemy import _SignallingSession

from flask_sqlalchemy import orm, partial, get_state


class _BindingKeyPattern(object):
    def __init__(self, db, pattern):
        self.db = db
        self.raw_pattern = pattern
        self.compiled_pattern = re.compile(pattern)
        self._shard_keys = None

    def __repr__(self):
        return "%s(pattern=%s)" % (self.__class__.__name__, self.raw_pattern)

    def match(self, key):
        return self.compiled_pattern.match(key)

    def get_shard_key(self, hash_num):
        if self._shard_keys is None:
            self._shard_keys = [
                key for key, value in self.db.
                app.config['SQLALCHEMY_BINDS'].iteritems()
                if self.compiled_pattern.match(key)]

            self._shard_keys.sort()

        return self._shard_keys[hash_num % len(self._shard_keys)]


class _BindingContext(object):
    def __init__(self, db_session_cls, name):
        self.db_session = db_session_cls()
        self.name = name

    def __enter__(self):
        self.db_session.push_binding(self.name)

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.db_session.pop_binding()
        self.db_session.close()


class _Session(_SignallingSession):
    def __init__(self, *args, **kwargs):
        _SignallingSession.__init__(self, *args, **kwargs)
        self._binding_keys = []
        self._binding_key = None

    def push_binding(self, key):
        self._binding_keys.append(self._binding_key)
        self._binding_key = key

    def pop_binding(self):
        self._binding_key = self._binding_keys.pop()

    def get_bind(self, mapper, clause=None):
        binding_key = self.__find_binding_key(mapper)
        if binding_key is None:
            return _SignallingSession.get_bind(self, mapper, clause)
        else:
            state = get_state(self.app)
            return state.db.get_engine(self.app, bind=binding_key)

    def __find_binding_key(self, mapper):
        if mapper is None:  # 맵퍼 없음
            return self._binding_key
        else:
            mapper_info = getattr(mapper.mapped_table, 'info', {})
            mapped_binding_key = mapper_info.get('bind_key')

            # 맵핑된 바인딩이 없으면 디폴트 바인딩
            if not mapped_binding_key:
                return self._binding_key

            # 정적 바인딩
            if type(mapped_binding_key) is str:
                return mapped_binding_key

            # 동적 바인딩
            if mapped_binding_key.match(self._binding_key):
                return self._binding_key

            # 푸쉬된 바인딩
            for pushed_binding_key in reversed(self._binding_keys):
                if pushed_binding_key and \
                        mapped_binding_key.match(pushed_binding_key):
                    return pushed_binding_key
            else:
                raise Exception(
                    'NOT_FOUND_MAPPED_BINDING:%s '
                    'CURRENT_BINDING:%s '
                    'PUSHED_BINDINGS:%s' % (
                        repr(mapped_binding_key),
                        repr(self._binding_key),
                        repr(self._binding_keys[1:])))


class Database(SQLAlchemy):
    def bind_key_pattern(self, pattern):
        return _BindingKeyPattern(self, pattern)

    def bind_key(self, key):
        return _BindingContext(self.session, key)

    def create_scoped_session(self, options=None):
        if options is None:
            options = {}

        scope_func=options.pop('scopefunc', None)
        return orm.scoped_session(
            partial(_Session, self, **options), scopefunc=scope_func
        )

    def get_binds(self, app=None):
        ret_binds = SQLAlchemy.get_binds(self, app)

        bind = None
        engine = self.get_engine(app, bind)
        tables = self.get_tables_for_bind(bind)
        ret_binds.update(dict((table, engine) for table in tables))
        return ret_binds

    def get_tables_for_bind(self, bind=None):
        result = []
        for table in self.Model.metadata.tables.itervalues():
            table_bind_key = table.info.get('bind_key')
            if table_bind_key == bind:
                result.append(table)
            else:
                if bind:
                    if type(table_bind_key) is _BindingKeyPattern and table_bind_key.match(bind):
                        result.append(table)
                    elif type(table_bind_key) is str and table_bind_key == bind:
                        result.append(table)

        return result


if __name__ == '__main__':
    import os

    from flask import Flask

    def main():
        app = Flask(__name__)
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        app.config['SQLALCHEMY_BINDS'] = {
            'data_1': 'sqlite:///:memory:',
            'data_2': 'sqlite:///:memory:',
            'log': 'sqlite:///:memory:'
        }

        db = Database(app)

        class User(db.Model):
            __bind_key__ = db.bind_key_pattern('data_\d')

            id = db.Column(db.Integer, primary_key=True)
            nickname = db.Column(db.String(64), index=True, unique=True)

            def __repr__(self):
                return "<User nickname='%s'>" % self.nickname

        class UserLog(db.Model):
            __bind_key__ = 'log'

            id = db.Column(db.Integer, primary_key=True)
            msg = db.Column(db.String(64))

        if not os.access('temp/test', os.R_OK):
            os.makedirs('temp/test')

        db.drop_all()
        db.create_all()

        with db.bind_key('data_1'):
            user = User(nickname='a')
            db.session.add(user)
            db.session.commit()

        with db.bind_key('data_2'):
            user = User(nickname='b')
            db.session.add(user)
            db.session.commit()

        user_log = UserLog(msg='x')
        db.session.add(user_log)
        db.session.commit()

        with db.bind_key('data_1'):
            print User.query.all()

        with db.bind_key('data_2'):
            print User.query.all()

    main()
