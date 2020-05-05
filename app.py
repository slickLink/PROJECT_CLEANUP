#imports
from flask import Flask


#initializations
app = Flask(__name__)


#routes
@app.route('/')
def index():
    return 'Hello, World!'