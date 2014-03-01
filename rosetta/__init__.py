import os

from framework import db, env

from framework import Flask

class ApplicationFactory(object):
    @staticmethod
    def __create_app(config_paths):
        app = Flask(__name__)

        env.init_app(app, __file__, config_paths)
        env.create_all()

        db.init_app(app)
        db.app = app # http://piotr.banaszkiewicz.org/blog/2012/06/29/flask-sqlalchemy-init_app/
        
        db.create_all()
        return app

    def create_main_app(self):
        return self.__create_app(config_paths=[
                '$APP_DIR/data/base_config.yml',
                '$PWD/active_config.yml'])

os.environ['APP_DIR'] = os.path.dirname(os.path.realpath(__file__))

app_factory = ApplicationFactory()

