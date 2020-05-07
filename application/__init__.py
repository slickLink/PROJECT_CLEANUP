#imports
from flask import Flask
from flask_session import Session
from config import Config

#initializations
app = Flask(__name__)
app.config.from_object(Config)
Session(app)

from application import routes, oauth, utils