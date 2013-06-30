import os
from flask import Flask
app = Flask(__name__)

log_file_path = os.path.abspath('whoperator.log')

import libs  # adds libs directory to path

import views
import api
