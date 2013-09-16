from flask import jsonify
from whoperator import app, db
from whoperator.models.schema import Artist
from whoperator.whatmanager import what_api


@app.route('/artist_info/<int:artist_id>')
def artist_info(artist_id):
    app.logger.debug("Getting artist_info for %s" % artist_id)
    try:
        # get artist from db
        db_artist_item = Artist.query.filter(Artist.what_id == artist_id).first()

        if not db_artist_item:
            app.logger.debug("Artist was not in db, querying API cache...")

            what_artist_item = what_api().get_artist(artist_id)
            if not what_artist_item.fully_loaded:
                app.logger.debug("Artist was not fully loaded...updating data")
                what_artist_item.update_data()

            db_artist_item = Artist(what_artist=what_artist_item)
            db.session.add(db_artist_item)
            db.session.commit()
    except Exception as e:
        return jsonify({'error': "%s -- %s" % (type(e), str(e))})

    if db_artist_item:
        return jsonify({'artist_info': db_artist_item.as_dict()})
    else:
        app.logger.debug("Artist doesn't exist.")
        return jsonify({'error': "Artist does not exist."})
