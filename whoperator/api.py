import calendar
import time
from datetime import datetime
import os
import json

from whoperator import app, LOG_FILE_PATH
from flask import request, Response, redirect, url_for, jsonify, stream_with_context

from whatmanager import what_api


### LOGGING STREAM
@app.route('/log')
def stream_log():
    def log_events():
        pos = 0
        event_id = 0
        last_heartbeat = time.time()
        while True:
            output = ""
            with open(LOG_FILE_PATH) as log_file:
                if pos > os.path.getsize(LOG_FILE_PATH):
                    pos = 0
                log_file.seek(pos)
                line = log_file.readline()
                line_elements = line.split(' - ')
                pos = log_file.tell()

                if line:
                    output = str(json.dumps({'type': 'log',
                                             'text': line_elements[-1].strip(),
                                             'id': event_id,
                                             'date': time.mktime(time.strptime(line_elements[0], "%Y-%m-%d %H:%M:%S"))}))
                    event_id += 1
                else:
                    if time.time() - last_heartbeat >= 10:
                        last_heartbeat = time.time()
                        output = str(json.dumps({'type': 'heartbeat', 'text': '--tick--', 'id': event_id, 'date': time.time()}))
                        event_id += 1
                    else:
                        time.sleep(0.1)
                yield output
                continue

    return Response(log_events(), content_type='application/json')


@app.route('/new_releases')
def new_releases():
    response = what_api().get_top_10(type='torrents', limit=10)
    past_day = response[0]['results']

    unique_group_ids = []
    unique_items = []
    for item in past_day:
        if item.group.id not in unique_group_ids:
            unique_group_ids.append(item.group.id)
            unique_items.append(item)
            if not item.group.has_complete_torrent_list:
                item.group.update_group_data()

    cleaned_results = [
        {'title': item.group.name,
         'artist_name': item.group.music_info['artists'][0].name,
         'group_id': item.group.id}
        for item in unique_items]
    return jsonify({'new_releases': cleaned_results})

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


@app.route('/collection/<int:collection_id>', methods=['PUT'])
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


@app.route('/collection/<int:collection_id>/item/<int:item_id>', methods=['PUT'])
def modify_collection_item(collection_id, item_id):
    pass


@app.route('/collection/<int:collection_id>/item/<int:item_id>', methods=['DELETE'])
def delete_collection_item(collection_id, item_id):
    pass
