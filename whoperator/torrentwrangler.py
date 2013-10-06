import os
from bencode import bencode, bdecode
from hashlib import sha1
from whoperator import db, app
from whoperator.models.schema import Torrent, TorrentFile, Artist, TorrentGroup
from whoperator.whatmanager import what_api


class TorrentFileReader:
    def __init__(self, file_path):
        self.file_path = file_path
        self.read_contents()

    def get_tracker(self):
        return self.contents['announce']

    def get_info_hash(self):
        return sha1(bencode(self.contents['info'])).hexdigest()

    def read_contents(self):
        with open(self.file_path, 'rb') as f:
            self.contents = bdecode(f.read())


class TorrentValidator:
    def __init__(self, gazelle_api):
        self.gazelle_api = gazelle_api

    def locate_source(self, torrent_file):
        info_hash = torrent_file.info_hash
        self.search_info_hash(info_hash)

    def search_info_hash(self, info_hash):
        self.gazelle_api.search_torrents(searchstr=info_hash)

    def hash_is_valid_torrent(self, hash):
        pass


def read_torrent_file_and_populate_db(path, context):
    torrent_reader = TorrentFileReader(path)

    collection_id = context['collection_id']
    size = os.path.getsize(path)
    rel_path = os.path.relpath(path, start=context['directory_path'])
    info_hash = torrent_reader.get_info_hash()

    # Load torrent file db item to see if we know this torrent already
    torrent_file_db_item = TorrentFile.query.filter_by(collection_id=collection_id, info_hash=info_hash).first()

    # Check to see if torrent is on What.cd
    what_torrent = what_api().get_torrent_from_info_hash(info_hash)

    if what_torrent is not None:
        # Torrent file db item
        if torrent_file_db_item is None:  # torrent file is on what but not in our db
            torrent_file_db_item = TorrentFile(collection_id, what_torrent.id, size, rel_path, info_hash)
            db.session.add(torrent_file_db_item)

        # Torrent db item
        torrent_db_item = Torrent.query.get(what_torrent.id)
        if torrent_db_item is None:
            torrent_db_item = Torrent(what_torrent)
            db.session.add(torrent_db_item)
        else:
            torrent_db_item.update_from_what(what_torrent)

        # TorrentGroup db item
        torrent_group_db_item = torrent_db_item.torrent_group
        if torrent_group_db_item:
            torrent_group_db_item.update_from_what(what_torrentgroup=what_torrent.group)
        else:
            torrent_group_db_item = TorrentGroup(what_torrentgroup=what_torrent.group)
        db.session.add(torrent_group_db_item)

        # Artist db item
        what_artists = what_torrent.group.music_info['artists'] + what_torrent.group.music_info['with']
        for what_artist in what_artists:
            artist_db_item = Artist.query.filter(Artist.what_id == what_artist.id).first()
            if not artist_db_item:
                if not what_artist.fully_loaded:
                    # TODO: deferred artist lookup
                    app.logger.debug("Need to scan for artist: %s, %s" % (what_artist.id, what_artist.name))
                    what_artist.update_data()

                artist_db_item = Artist(what_artist=what_artist)
                artist_db_item.torrent_groups.append(torrent_group_db_item)
                db.session.add(artist_db_item)

        db.session.commit()
    else:
        if torrent_file_db_item is None:  # torrent file is not on what, but we need to add to our db anyway
            torrent_file_db_item = TorrentFile(collection_id, -1, size, rel_path, info_hash)
            db.session.add(torrent_file_db_item)
            db.session.commit()

    return None
