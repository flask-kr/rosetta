from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_ext_environment import Environment

class ServerManager(object):
    class Error(Exception):
        pass

    def __init__(self):
        self.app = Flask(__name__)
        self.env = Environment(self.app)
        self.db = SQLAlchemy(self.app)

    def create_all(self):
        self.env.create_all()
        self.db.create_all()
        return self

    def reset_all_databases(self):
        self.db.drop_all() 
        self.db.create_all()

    def run_server(self, port=5000, ip='0.0.0.0'):
        self.app.run(ip, port=port)

