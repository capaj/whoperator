from flask import jsonify
from pygazelle.api import LoginException
from whoperator import app
from whoperator.whatmanager import what_api, what_invalidate_instance


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
        for item in unique_items if item.group.music_info is not None]
    return jsonify({'new_releases': cleaned_results})


@app.route('/validate_what_login')
def validate_what_login():
    what_invalidate_instance()

    try:
        what_api()._login()
        return jsonify({'status': "success",
                        'user': what_api().logged_in_user.__dict__()})
    except Exception:
        return jsonify({'status': "failure"})
