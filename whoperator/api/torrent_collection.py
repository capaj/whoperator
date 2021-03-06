import os
from datetime import datetime
from whoperator import app, db, filescanner, torrentwrangler
from whoperator.models.schema import TorrentFileCollection, TorrentFile, Torrent
from flask import jsonify, request


@app.route('/torrent_collection')
def list_torrent_collections():
    limit = int(request.args.get('limit', 0))
    offset = int(request.args.get('offset', 0))

    total_records = TorrentFileCollection.query.count()

    if limit > 0:
        results = TorrentFileCollection.query.limit(limit).offset(offset)
    else:
        results = TorrentFileCollection.query.offset(offset).all()

    result_dict = {
        'collections': [item.as_dict() for item in results],
        'limit': limit,
        'offset': offset,
        'total': total_records
    }

    return jsonify(result_dict)


@app.route('/torrent_collection/<int:collection_id>')
def show_torrent_collection(collection_id):
    collection_db_item = TorrentFileCollection.query.get(collection_id)

    if collection_db_item is None:
        response = jsonify({'error': 'Unknown collection ID.'})
        response.status_code = 500
        return response

    return jsonify({collection_db_item.id: collection_db_item.as_dict()})


@app.route('/torrent_collection', methods=['POST'])
def add_torrent_collection():
    path = request.form.get('path', None)
    name = request.form.get('name', None)
    scan = request.form.get('scan', True) in ('true', 'True', '1', True)
    recurse = request.form.get('recurse', True) in ('true', 'True', '1', True)

    if path is None or not os.path.isdir(path):
        response = jsonify({'error': 'Path does not exist.'})
        response.status_code = 500
        return response

    new_collection = TorrentFileCollection(name, path, recurse)
    db.session.add(new_collection)
    db.session.commit()

    if scan:
        scanner_context = {'collection_id': new_collection.id, 'directory_path': path}

        filescanner.set_global_filetype_handler("*.torrent", torrentwrangler.read_torrent_file_and_populate_db)
        filescanner.scan_directory(directory_path=path,
                                   file_data_callback=None,
                                   context=scanner_context,
                                   filetype_filter="*.torrent",
                                   recurse=recurse,
                                   priority=False)

    return jsonify({new_collection.id: new_collection.as_dict()})


@app.route('/torrent_collection/<int:collection_id>', methods=['PUT'])
def modify_torrent_collection(collection_id):
    collection_db_item = TorrentFileCollection.query.get(collection_id)

    if collection_db_item is None:
        response = jsonify({'error': 'Unknown collection ID.'})
        response.status_code = 500
        return response

    path = request.form.get('path', None)
    name = request.form.get('name', None)

    path_changed = (path is not None and path != collection_db_item.path)
    if path_changed:
        if os.path.isdir(path):
            collection_db_item.path = path
        else:
            response = jsonify({'error': 'Path does not exist.'})
            response.status_code = 500
            return response

    recurse_default = collection_db_item.recurse

    name_changed = (name is not None and name != collection_db_item.name)
    if name_changed:
        collection_db_item.name = name

    recurse = request.form.get('recurse', recurse_default) in ('true', 'True', '1', True)
    recurse_changed = (recurse != collection_db_item.recurse)
    if recurse_changed:
        collection_db_item.recurse = recurse

    if path_changed or name_changed or recurse_changed:
        collection_db_item.updated = datetime.now()
        db.session.commit()

    scan_default = path_changed or recurse_changed

    scan = request.form.get('scan', scan_default) in ('true', 'True', '1', True)
    if scan:
        # nuke existing collection files, rescan
        old_torrentfiles = TorrentFile.query.filter(TorrentFile.collection_id == collection_id)
        old_torrentfiles.delete()
        db.session.commit()

        scanner_context = {'collection_id': collection_id, 'directory_path': collection_db_item.path}
        filescanner.set_global_filetype_handler("*.torrent", torrentwrangler.read_torrent_file_and_populate_db)
        filescanner.scan_directory(directory_path=collection_db_item.path,
                                   file_data_callback=None,
                                   context=scanner_context,
                                   filetype_filter="*.torrent",
                                   recurse=collection_db_item.recurse,
                                   priority=False)

    return jsonify({collection_db_item.id: collection_db_item.as_dict()})


@app.route('/torrent_collection/<int:collection_id>', methods=['DELETE'])
def delete_torrent_collection(collection_id):
    try:
        collection_db_item = TorrentFileCollection.query.get(collection_id)

        if collection_db_item is None:
            response = jsonify({'error': 'Unknown collection ID.'})
            response.status_code = 500
            return response

        name = collection_db_item.name
        db.session.delete(collection_db_item)
        db.session.commit()
        return jsonify({'result': "Deleted Torrent File Collection '%s', id: %s" % (name, collection_id)})
    except Exception as e:
        db.session.rollback()
        return jsonify({'result': "Failed to delete Torrent File Collection. Exception: %s" % e})


### ITEM CRUD

@app.route('/torrent_collection/<int:collection_id>/item')
def list_torrent_collection_items(collection_id):
    limit = int(request.args.get('limit', 0))
    offset = int(request.args.get('offset', 0))

    collection_db_item = TorrentFileCollection.query.get(collection_id)

    if collection_db_item is None:
        response = jsonify({'error': 'Unknown collection ID.'})
        response.status_code = 500
        return response

    total_records = TorrentFile.query.filter(TorrentFile.collection_id == collection_id).count()

    if limit > 0:
        torrent_files = TorrentFile.query.filter(TorrentFile.collection_id == collection_id).limit(limit).offset(offset)
    else:
        torrent_files = TorrentFile.query.filter(TorrentFile.collection_id == collection_id).offset(offset)

    # Do we want more info here? Not adding torrent and artist info to reduce db access, but we could do it...
    items = [{'collection_id': item.collection_id,
              'torrent_id': item.torrent_id,
              'torrent_file_id': item.id,
              'size': item.size,
              'file_exists': os.path.isfile(os.path.join(collection_db_item.path, item.rel_path)),
              'full_path': os.path.join(collection_db_item.path, item.rel_path),
              'rel_path': item.rel_path,
              'info_hash': item.info_hash} for item in torrent_files]

    result_dict = {
        'items': items,
        'limit': limit,
        'offset': offset,
        'total': total_records
    }

    return jsonify(result_dict)


@app.route('/torrent_collection/<int:collection_id>/item/<int:item_id>')
def show_torrent_collection_item(collection_id, item_id):
    collection_db_item = TorrentFileCollection.query.get(collection_id)

    if collection_db_item is None:
        response = jsonify({'error': 'Unknown collection ID.'})
        response.status_code = 500
        return response

    file_db_item = TorrentFile.query.get(item_id)

    if file_db_item is None:
        response = jsonify({'error': 'Unknown file item ID.'})
        response.status_code = 500
        return response

    if file_db_item.collection_id != collection_db_item.id:
        response = jsonify({'error': 'Item not in specified collection.'})
        response.status_code = 500
        return response

    full_path = os.path.join(collection_db_item.path, file_db_item.rel_path)

    if file_db_item.torrent_id > 0:
        torrent = Torrent.query.get(file_db_item.torrent_id)
        torrent_details = torrent.as_dict()
        if torrent is None:
            response = jsonify({'error': "Couldn't load torrent details."})
            response.status_code = 500
            return response
    else:
        torrent_details = {}

    result_dict = {file_db_item.id:
                         {'collection_id': file_db_item.collection_id,
                          'collection': collection_db_item.as_dict(),
                          'on_what': file_db_item.id != -1,
                          'torrent_id': file_db_item.torrent_id,
                          'torrent': torrent_details,
                          'size': file_db_item.size,
                          'file_exists': os.path.isfile(full_path),
                          'full_path': full_path,
                          'rel_path': file_db_item.rel_path,
                          'info_hash': file_db_item.info_hash}}
    return jsonify(result_dict)

# @app.route('/collection/<int:collection_id>/item/', methods=['POST'])
# def add_collection_item(collection_id, item_id):
#     pass
#
#
# @app.route('/collection/<int:collection_id>/item/<int:item_id>', methods=['PUT'])
# def modify_collection_item(collection_id, item_id):
#     pass


@app.route('/collection/<int:collection_id>/item/<int:item_id>', methods=['DELETE'])
def delete_torrent_collection_item(collection_id, item_id):
    pass
