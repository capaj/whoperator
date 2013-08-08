from flask import redirect, jsonify
from whoperator import app
from whoperator.whatmanager import what_api


@app.route('/torrent_file/<int:torrent_id>')
def torrent_file(torrent_id):
    app.logger.debug("Determining URL for torrent file %s" % torrent_id)
    try:
        return redirect(what_api().generate_torrent_link(torrent_id))
    except Exception as e:
        return jsonify({'error': str(e)})
