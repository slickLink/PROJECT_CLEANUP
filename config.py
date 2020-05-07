import os, redis
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))

class Config(object):

    #General Configurations
    SECRET_KEY = os.getenv('SECRET_KEY') or 'you-shall-not-pass'

    #Spotify Configurations
    CLIENT_ID = os.getenv('CLIENT_ID') or 'oops'
    CLIENT_SECRET = os.getenv('CLIENT_SECRET') or 'oops'
    REDIRECT_URI = os.getenv('REDIRECT_URI') or 'opps'
    
    #Redis configurations
    SESSION_TYPE = os.getenv('SESSION_TYPE')
    SESSION_REDIS = redis.from_url(os.getenv('SESSION_REDIS'))

