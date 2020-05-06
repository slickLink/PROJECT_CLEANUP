#imports
from flask import Flask
from config import Config

#initializations
app = Flask(__name__)
app.config.from_object(Config)

from application import routes, oauth, utils