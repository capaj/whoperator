from collections import deque
import os, shutil
from flask import Flask
from flask.signals import Namespace
app = Flask(__name__)

CONFIG_PATH = os.environ.get(os.path.abspath('WHOPERATOR_CFG_PATH'), os.path.abspath('whoperator.cfg'))

if not os.path.exists(CONFIG_PATH):
    shutil.copyfile('whoperator.default.cfg', CONFIG_PATH)

app.config.from_pyfile(CONFIG_PATH)

LOG_FILE_PATH = os.path.abspath('whoperator.log')
log_history = deque([], maxlen=50)

import libs  # adds libs directory to path

import views
import api
