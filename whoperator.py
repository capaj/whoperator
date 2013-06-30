import logging
from logging.handlers import RotatingFileHandler
from whoperator import app, LOG_FILE_PATH


log_file_handler = RotatingFileHandler(LOG_FILE_PATH, maxBytes=1024**2 * 100, backupCount=5)
log_file_handler.setLevel(logging.DEBUG)
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s", "%Y-%m-%d %H:%M:%S")
log_file_handler.setFormatter(formatter)

app.logger.addHandler(log_file_handler)


if __name__ == "__main__":
    app.run(debug=True, threaded=True)
