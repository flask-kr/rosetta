import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_ext_environment import Environment

db = SQLAlchemy()
env = Environment()

