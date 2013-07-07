from collections import deque
import os, shutil

import libs  # adds libs directory to path

from flask import Flask
import models.schema
from models.schema import db as db

app = Flask(__name__)

CONFIG_PATH = os.environ.get(os.path.abspath('WHOPERATOR_CFG_PATH'), os.path.abspath('whoperator.cfg'))

if not os.path.exists(CONFIG_PATH):
    shutil.copyfile('whoperator.default.cfg', CONFIG_PATH)

app.config.from_pyfile(CONFIG_PATH)

# Set up logging
LOG_FILE_PATH = os.path.abspath(app.config.get('LOG_LOCATION', 'whoperator.log'))
log_history = deque([], maxlen=50)

# Set up DB
def setup_db():
    app.config.setdefault('SQLALCHEMY_DATABASE_URI', "sqlite:///../whoperator.db")
    db.init_app(app)
    ctx = app.test_request_context()
    ctx.push()
    db.engine.echo = True
    db.create_all()
    ctx.pop()

setup_db()

# Import all the routes
import views
import api
