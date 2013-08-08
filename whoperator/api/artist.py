from flask import jsonify
from whoperator import app
from whoperator.whatmanager import what_api


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
