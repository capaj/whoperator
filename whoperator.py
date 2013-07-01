import logging
from logging.handlers import RotatingFileHandler
from whoperator import app, LOG_FILE_PATH, log_history


class LogHistoryHandler(logging.Handler):
    def __init__(self, history_deque):
        logging.Handler.__init__(self)
        self.level = logging.DEBUG
        self.history_deque = history_deque

    def emit(self, record):
        try:
            self.history_deque.append(record)
        except (KeyboardInterrupt, SystemExit):
            raise
        except:
            self.handleError(record)

log_file_formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s", "%Y-%m-%d %H:%M:%S")

log_file_handler = RotatingFileHandler(LOG_FILE_PATH, maxBytes=1024**2 * 100, backupCount=5)
log_file_handler.setLevel(logging.DEBUG)
log_file_handler.setFormatter(log_file_formatter)

log_history_handler = LogHistoryHandler(history_deque=log_history)
log_history_handler.setLevel(logging.DEBUG)

app.logger.addHandler(log_file_handler)
app.logger.addHandler(log_history_handler)

if __name__ == "__main__":
    app.run(debug=True, threaded=True)
