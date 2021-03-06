from flask import jsonify, request
from sqlalchemy.orm import joinedload
from whoperator import app, db
from whoperator.models.schema import Artist, TorrentGroup
from whoperator.whatmanager import what_api


@app.route('/artist')
def list_artists():
    # TODO: arguments when listing to limit to artists in a torrent collection or media collection
    app.logger.debug("Listing artists...")

    limit = int(request.args.get('limit', 0))
    offset = int(request.args.get('offset', 0))

    # TODO: optimize counting to only happen when needed...can just grab length of results if listing all()
    total_records = Artist.query.count()

    if limit > 0:
        results = Artist.query.limit(limit).offset(offset)
    else:
        results = Artist.query.offset(offset).all()

    result_dict = {
        'artists': [item.as_dict() for item in results],
        'limit': limit,
        'offset': offset,
        'total': total_records
    }

    return jsonify(result_dict)


@app.route('/artist/<int:artist_id>', defaults={'is_what_id': False})
@app.route('/what_artist/<int:artist_id>', defaults={'is_what_id': True})
def what_artist_info(artist_id, is_what_id):
    app.logger.debug("Getting what artist info for %s" % artist_id)
    lookup = request.args.get('lookup', False) in ('true', 'True', '1', True)

    # get artist from db
    if is_what_id:
        db_artist_item = Artist.query.filter(Artist.what_id == artist_id).first()
    else:
        db_artist_item = Artist.query.filter(Artist.id == artist_id).first()

    if is_what_id and lookup and not db_artist_item:
        try:
            app.logger.debug("Artist was not in db, querying API cache...")

            what_artist_item = what_api().get_artist(artist_id)
            if not what_artist_item.fully_loaded:
                app.logger.debug("Artist was not fully loaded...updating data")
                what_artist_item.update_data()

            db_artist_item = Artist(what_artist=what_artist_item)

            for what_torrentgroup in what_artist_item.torrent_groups:
                db_torrent_group = TorrentGroup(what_torrentgroup=what_torrentgroup)
                db_artist_item.torrent_groups.append(db_torrent_group)
                db.session.add(db_torrent_group)

            db.session.add(db_artist_item)
            db.session.commit()
        except Exception as e:
            app.logger.exception(e)
            return jsonify({'error': "%s -- %s" % (type(e), str(e))})

    if db_artist_item:
        artist_dict = db_artist_item.as_dict()
        artist_dict['torrent_groups'] = [group.as_dict() for group in db_artist_item.torrent_groups]
        return jsonify({'artist_info': artist_dict})
    elif not lookup:
        app.logger.debug("Artist not in database. Try again with a what id and lookup enabled to search remotely.")
        return jsonify({'error': "Artist not in database. Try again with a what id and lookup enabled to search remotely."})
    else:
        app.logger.debug("Artist unknown.")
        return jsonify({'error': "Artist unknown."})
