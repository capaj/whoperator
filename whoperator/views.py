from whoperator import app

from flask import render_template

@app.route('/')
def home():
    app.logger.info("butts")
    return render_template('index.html')
