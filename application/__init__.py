import os

from flask import Flask

APPLICATION_DIR_PATH = os.path.dirname(os.path.realpath(__file__))
PROJECT_DIR_PATH = os.path.dirname(APPLICATION_DIR_PATH)

os.environ['APPLICATION_DIR'] = APPLICATION_DIR_PATH
os.environ['PROJECT_DIR'] = PROJECT_DIR_PATH


class ApplicationFactory(object):
    @staticmethod
    def create_application(
            default_config_file_path,
            custom_config_file_path='',
            custom_config_dict={}):

        app = Flask(__name__)

        from framework import env
        env.init_app(app)
        env.load_config_file(default_config_file_path)

        if custom_config_file_path:
            env.load_config_file(custom_config_file_path)

        if custom_config_dict:
            env.load_config_dict(custom_config_dict)

        env.create_all()

        from framework import db
        db.init_app(app)
        db.app = app

        import models
        if app.config['DB_CREATE_ALL']:
            db.create_all()

        from apis import api_bp
        app.register_blueprint(api_bp)

        @app.route('/')
        def get_home():
            return 'rosetta service'

        return app

app_factory = ApplicationFactory()

