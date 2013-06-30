import os, shutil
from flask import Flask
app = Flask(__name__)

CONFIG_PATH = os.environ.get(os.path.abspath('WHOPERATOR_CFG_PATH'), os.path.abspath('whoperator.cfg'))

if not os.path.exists(CONFIG_PATH):
    shutil.copyfile('whoperator.default.cfg', CONFIG_PATH)

app.config.from_pyfile(CONFIG_PATH)

LOG_FILE_PATH = os.path.abspath('whoperator.log')

import libs  # adds libs directory to path

import views
import api
