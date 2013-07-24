import os
from bencode import bencode, bdecode
from hashlib import sha1
from whoperator import db
from whoperator.models.schema import Torrent
from whoperator.whatmanager import what_api



class TorrentFile:
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


def read_torrent_file_for_db(path, context):
    torrent = TorrentFile(path)

    collection_id = context['collection_id']
    size = os.path.getsize(path)
    rel_path = os.path.relpath(path, start=context['directory_path'])
    info_hash = torrent.get_info_hash()

    what_torrent = what_api().get_torrent_from_info_hash(info_hash)

    if what_torrent is not None:
        torrent_db_item = Torrent.query.get(what_torrent.id)
        if torrent_db_item is None:
            torrent_db_item = Torrent(what_torrent)
            db.session.add(torrent_db_item)
            db.session.commit()

        return collection_id, torrent_db_item.id, size, rel_path, info_hash
    else:
        return None
