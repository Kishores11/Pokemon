import os
from configparser import ConfigParser

config = ConfigParser()
config.read(os.path.join(os.path.dirname(__file__), '..', 'serverbase.cfg'))

DEBUG = config.getboolean('FLASK', 'DEBUG')
SECRET_KEY = config.get('FLASK', 'SECRET_KEY')
SQLALCHEMY_DATABASE_URI = config.get('FLASK', 'SQLALCHEMY_DATABASE_URI')
PAGE_LIMIT = config.getint('FLASK', 'PAGE_LIMIT')
