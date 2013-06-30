import time
import os

from whoperator import app, log_file_path
from flask import request, Response, redirect, url_for


### LOGGING STREAM
@app.route('/log')
def stream_log():
    def log_events():
        pos = 0
        while True:
            with open(log_file_path) as log_file:
                if pos > os.path.getsize(log_file_path):
                    pos = 0
                log_file.seek(pos)
                line = log_file.readline()
                pos = log_file.tell()
                if not line:
                    time.sleep(0.1)
                    continue
                yield line
    return Response(log_events(), content_type='text/event-stream')

### COLLECTION CRUD

@app.route('/collection/')
def list_collections():
    pass


@app.route('/collection/<int:collection_id>')
def show_collection(collection_id):
    pass


@app.route('/collection/', methods=['POST'])
def add_collection():
    pass


@app.route('/collection/<int:collection_id>', methods=['POST', 'PUT'])
def modify_collection(collection_id):
    pass


@app.route('/collection/<int:collection_id>', methods=['DELETE'])
def delete_collection(collection_id):
    pass


### ITEM CRUD

@app.route('/collection/<int:collection_id>/item')
def list_collection_items(collection_id):
    pass


@app.route('/collection/<int:collection_id>/item/<int:item_id>')
def show_collection_item(collection_id, item_id):
    pass


@app.route('/collection/<int:collection_id>/item/', methods=['POST'])
def add_collection_item(collection_id, item_id):
    pass


@app.route('/collection/<int:collection_id>/item/<int:item_id>', methods=['POST', 'PUT'])
def modify_collection_item(collection_id, item_id):
    pass


@app.route('/collection/<int:collection_id>/item/<int:item_id>', methods=['DELETE'])
def delete_collection_item(collection_id, item_id):
    pass
