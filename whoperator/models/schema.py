from datetime import datetime
from pygazelle import media, format, encoding

from whoperator import db


### What.cd Objects

class Artist(db.Model):
    __tablename__ = 'artist'

    id = db.Column(db.Integer, primary_key=True)

    what_id = db.Column(db.Integer, index=True)
    name = db.Column(db.String(length=255))
    image = db.Column(db.Text)
    body = db.Column(db.Text)
    vanity_house = db.Column(db.Boolean)
    created = db.Column(db.TIMESTAMP)
    updated = db.Column(db.TIMESTAMP)


class TorrentGroup(db.Model):
    __tablename__ = 'torrent_group'

    id = db.Column(db.Integer, primary_key=True)

    what_id = db.Column(db.Integer, index=True)
    name = db.Column(db.String(length=255))

    # use db id, not what_id
    artist_id = db.Column(db.Integer, db.ForeignKey('artist.id'))
    artist = db.relationship(Artist, primaryjoin=artist_id == Artist.id,
                             backref=db.backref("torrent_groups", cascade="all,delete"))

    wiki_body = db.Column(db.Text)
    wiki_image = db.Column(db.Text)
    year = db.Column(db.Integer)
    record_label = db.Column(db.String(length=100))
    catalogue_number = db.Column(db.String(length=100))
    vanity_house = db.Column(db.Boolean)
    last_mod_time = db.Column(db.DATETIME)

    created = db.Column(db.TIMESTAMP)
    updated = db.Column(db.TIMESTAMP)


class Torrent(db.Model):
    __tablename__ = 'torrent'

    id = db.Column(db.Integer, primary_key=True)

    # use db id, not what_id
    torrent_group_id = db.Column(db.Integer, db.ForeignKey('torrent_group.id'))
    torrent_group = db.relationship(TorrentGroup, primaryjoin=torrent_group_id == TorrentGroup.id,
                                    backref=db.backref("torrents", cascade="all,delete"))

    media = db.Column(db.Enum(*media.ALL_MEDIAS, name="media_types"))
    format = db.Column(db.Enum(*format.ALL_FORMATS, name="format_types"))
    encoding = db.Column(db.Enum(*encoding.ALL_ENCODINGS, name="encoding_types"))
    remaster_year = db.Column(db.Integer)
    remastered = db.Column(db.Boolean)
    remaster_title = db.Column(db.Text)
    remaster_record_label = db.Column(db.String(length=100))
    remaster_catalog_number = db.Column(db.String(length=100))
    scene = db.Column(db.Boolean)
    has_log = db.Column(db.Boolean)
    has_cue = db.Column(db.Boolean)
    log_score = db.Column(db.Integer)
    file_count = db.Column(db.Integer)
    free_torrent = db.Column(db.Boolean)
    size = db.Column(db.Integer)
    leechers = db.Column(db.Integer)
    seeders = db.Column(db.Integer)
    snatched = db.Column(db.Integer)
    last_mod_time = db.Column(db.DATETIME)
    has_file = db.Column(db.Boolean)
    description = db.Column(db.Text)
    file_path = db.Column(db.Text)
    created = db.Column(db.TIMESTAMP)
    updated = db.Column(db.TIMESTAMP)
    # user_id
    # username

    def __init__(self, what_torrent):
        self.id = what_torrent.id
        self.created = datetime.now()
        self.update_from_what(what_torrent)

    def update_from_what(self, what_torrent):
        if self.id != what_torrent.id:
            raise Exception("Tried to update Torrent id %s with data from id %s" % (self.id, what_torrent.id))

        self.torrent_group_id = what_torrent.group.id
        self.media = what_torrent.media
        self.format = what_torrent.format
        self.encoding = what_torrent.encoding
        self.remaster_year = what_torrent.remaster_year
        self.remastered = what_torrent.remastered
        self.remaster_title = what_torrent.remaster_title
        self.remaster_record_label = what_torrent.remaster_record_label
        self.remaster_catalogue_number = what_torrent.remaster_catalogue_number
        self.scene = what_torrent.scene
        self.has_log = what_torrent.has_log
        self.has_cue = what_torrent.has_cue
        self.log_score = what_torrent.log_score
        self.file_count = what_torrent.file_count
        self.free_torrent = what_torrent.free_torrent
        self.size = what_torrent.size
        self.leechers = what_torrent.leechers
        self.seeders = what_torrent.seeders
        self.snatched = what_torrent.snatched
        self.time = what_torrent.time
        self.has_file = what_torrent.has_file
        self.description = what_torrent.description
        self.file_path = what_torrent.file_path
        self.updated = datetime.now()


class Song(db.Model):
    __tablename__ = 'song'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(length=255))

    # use db id, not what_id
    artist_id = db.Column(db.Integer, db.ForeignKey('artist.id'))
    artist = db.relationship(Artist, primaryjoin=artist_id == Artist.id,
                             backref=db.backref("songs", cascade="all,delete"))

    torrent_group_id = db.Column(db.Integer, db.ForeignKey('torrent_group.id'))
    torrent_group = db.relationship(TorrentGroup, primaryjoin=torrent_group_id == TorrentGroup.id,
                                    backref=db.backref("songs", cascade="all,delete"))


### File Collection Objects
class TorrentFileCollection(db.Model):
    __tablename__ = 'torrent_file_collection'
    __public__ = ['name', 'path']

    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String(100))
    path = db.Column(db.Text)
    recurse = db.Column(db.Boolean)

    created = db.Column(db.TIMESTAMP)
    updated = db.Column(db.TIMESTAMP)

    def __init__(self, name, path, recurse):
        self.name = name
        self.path = path
        self.recurse = recurse
        self.created = self.updated = datetime.now()


class MediaFileCollection(db.Model):
    __tablename__ = 'media_file_collection'

    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String(100))
    path = db.Column(db.Text)
    recurse = db.Column(db.Boolean)

    created = db.Column(db.TIMESTAMP)
    updated = db.Column(db.TIMESTAMP)

    def __init__(self, name, path, recurse):
        self.name = name
        self.path = path
        self.recurse = recurse
        self.created = self.updated = datetime.now()


### File Objects
class TorrentFile(db.Model):
    __tablename__ = 'torrent_file'

    id = db.Column(db.Integer, primary_key=True)

    collection_id = db.Column(db.Integer, db.ForeignKey('torrent_file_collection.id'))
    collection = db.relationship(TorrentFileCollection, primaryjoin=collection_id == TorrentFileCollection.id,
                                 backref=db.backref("torrent_files", cascade="all,delete"))

    torrent_id = db.Column(db.Integer, db.ForeignKey('torrent.id'))
    torrent = db.relationship(Torrent, primaryjoin=torrent_id == Torrent.id)

    size = db.Column(db.Integer)
    rel_path = db.Column(db.Text)
    info_hash = db.Column(db.String(length=40), index=True)

    def __init__(self, collection_id, torrent_id, size, rel_path, info_hash, context=None):
        self.collection_id = collection_id
        self.torrent_id = torrent_id
        self.size = size
        self.rel_path = rel_path
        self.info_hash = info_hash


class MediaFile(db.Model):
    __tablename__ = 'media_file'

    id = db.Column(db.Integer, primary_key=True)

    collection_id = db.Column(db.Integer, db.ForeignKey('media_file_collection.id'))
    collection = db.relationship(MediaFileCollection, primaryjoin=collection_id == MediaFileCollection.id,
                                 backref=db.backref("media_files", cascade="all,delete"))

    song_id = db.Column(db.Integer, db.ForeignKey('song.id'))
    song = db.relationship(Song, primaryjoin=song_id == Song.id)

    torrent_file_id = db.Column(db.Integer, db.ForeignKey('torrent_file.id'))
    torrent_file = db.relationship(TorrentFile, primaryjoin=torrent_file_id == TorrentFile.id)

    size = db.Column(db.Integer)
    rel_path = db.Column(db.Text)
    mime_type = db.Column(db.Text)
    sha256 = db.Column(db.String(length=64))
