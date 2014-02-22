import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_ext_environment import Environment
from command_manager import CommandManager

db = SQLAlchemy()
env = Environment()
command_manager = CommandManager()

