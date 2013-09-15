from pygazelle.api import GazelleAPI
from whoperator import app

_what_api_instance = None


def what_api():
    global _what_api_instance
    if not _what_api_instance:
        _what_api_instance = GazelleAPI(username=app.config.get('WHAT_USER'), password=app.config.get('WHAT_PASS'))
    return _what_api_instance


def what_invalidate_instance():
    global _what_api_instance
    _what_api_instance = None
