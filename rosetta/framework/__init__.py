from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from environment import Environment

db = SQLAlchemy()
env = Environment()

