import os

from framework import db, env

from framework import Flask, Environment


class ApplicationFactory(object):
    @staticmethod
    def create_app(default_config_path, user_config_path=''):
        app = Flask(__name__)

        env.init_app(app)
        env.load_config_file(default_config_path)
        if user_config_path:
            env.load_config_file(user_config_path)

        env.create_all()

        db.init_app(app)
        db.app = app
        
        db.create_all()
        return app

os.environ['APP_DIR'] = os.path.dirname(os.path.realpath(__file__))

app_factory = ApplicationFactory()

