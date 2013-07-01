from whoperator import app, log_history
from flask import jsonify

from whatmanager import what_api


### LOGGING
@app.route('/log')
def log():
    def build_log(record_id, record):
        return {
            'type': 'log',
            'text': record.msg,
            'id': record_id,
            'date': record.asctime,
            'level': record.levelname
        }

    log_list = [build_log(record_id, record) for record_id, record in enumerate(log_history)]

    return jsonify({'json_log': log_list})


@app.route('/artist_info/<int:artist_id>')
def artist_info(artist_id):
    app.logger.debug("Getting artist_info for %s" % artist_id)
    try:
        artist_item = what_api().get_artist(artist_id)
        if not artist_item.fully_loaded:
            app.logger.debug("Artist was not fully loaded...updating data")
            artist_item.update_data()
    except Exception as e:
        return jsonify({'error': str(e)})

    return jsonify({'artist_info': artist_item.__dict__()})


@app.route('/new_releases')
def new_releases():
    app.logger.debug("Loading /new_releases")
    try:
        response = what_api().get_top_10(type='torrents', limit=10)
    except Exception as e:
        return jsonify({'error': str(e)})

    past_day = response[0]['results']

    unique_group_ids = []
    unique_items = []
    for item in past_day:
        if item.group.id not in unique_group_ids:
            unique_group_ids.append(item.group.id)
            unique_items.append(item)

    cleaned_results = [
        {
            'title': item.group.name,
            'artists': [{'name': artist.name} for artist in item.group.music_info['artists']],
            'torrent_group_id': item.group.id
        }
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
