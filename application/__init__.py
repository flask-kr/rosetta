import os

from framework import env
from framework import db

from framework import Flask


class ApplicationFactory(object):
    @staticmethod
    def create_app(default_config_path, user_config_path='', code_config_dict={}):
        app = Flask(__name__)

        env.init_app(app)
        env.load_config_file(default_config_path)
        if user_config_path:
            env.load_config_file(user_config_path)

        if code_config_dict:
            env.load_config_dict(code_config_dict)

        env.create_all()

        db.init_app(app)
        db.app = app

        import models
        db.create_all()

        import apis
        app.register_blueprint(apis.bp)

        return app

APPLICATION_DIR_PATH = os.path.dirname(os.path.realpath(__file__))
PROJECT_DIR_PATH = os.path.dirname(APPLICATION_DIR_PATH)

os.environ['APPLICATION_DIR'] = APPLICATION_DIR_PATH
os.environ['PROJECT_DIR'] = PROJECT_DIR_PATH

app_factory = ApplicationFactory()

