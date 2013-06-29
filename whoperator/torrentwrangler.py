import os
from bencode import bencode, bdecode
from hashlib import sha1



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


class TorrentFileCollection:
    def __init__(self, base_path):
        self.base_path = base_path

    def list_torrent_files(self):
        torrent_files = []
        for root, dirs, files in os.walk(self.base_path):
            for file in files:
                if file.endswith('.torrent'):
                    try:
                        torrent_files.append(TorrentFile(os.path.join(root, file)))
                    except Exception:
                        pass


        return torrent_files

    def list_files_and_info_hashes(self):
        return dict([(torrent_file.file_path, torrent_file.get_info_hash()) for torrent_file in self.list_torrent_files()])


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
