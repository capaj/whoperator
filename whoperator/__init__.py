from flask import Flask
app = Flask(__name__)

import libs  # adds libs directory to path

import views
import api
