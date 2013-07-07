from pygazelle import media, format, encoding
from flask.ext.sqlalchemy import SQLAlchemy

db = SQLAlchemy()


### What.cd Objects

class Artist(db.Model):
    __tablename__ = 'artist'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(length=255))
    image = db.Column(db.Text)
    body = db.Column(db.Text)
    vanity_house = db.Column(db.Boolean)
    created = db.Column(db.TIMESTAMP)
    updated = db.Column(db.TIMESTAMP)


class TorrentGroup(db.Model):
    __tablename__ = 'torrent_group'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(length=255))

    artist_id = db.Column(db.Integer, db.ForeignKey('artist.id'))
    artist = db.relationship(Artist, primaryjoin=artist_id == Artist.id)

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

    torrent_group_id = db.Column(db.Integer, db.ForeignKey('torrent_group.id'))
    torrent_group = db.relationship(TorrentGroup, primaryjoin=torrent_group_id == TorrentGroup.id)

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
    # user_id
    # username


class Song(db.Model):
    __tablename__ = 'song'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(length=255))

    artist_id = db.Column(db.Integer, db.ForeignKey('artist.id'))
    artist = db.relationship(Artist, primaryjoin=artist_id == Artist.id)

    torrent_group_id = db.Column(db.Integer, db.ForeignKey('torrent_group.id'))
    torrent_group = db.relationship(TorrentGroup, primaryjoin=torrent_group_id == TorrentGroup.id)


### File Collection Objects
class TorrentFileCollection(db.Model):
    __tablename__ = 'torrent_file_collection'

    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String(100))
    path = db.Column(db.Text)

    created = db.Column(db.TIMESTAMP)
    updated = db.Column(db.TIMESTAMP)


class MediaFileCollection(db.Model):
    __tablename__ = 'media_file_collection'

    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String(100))
    path = db.Column(db.Text)

    created = db.Column(db.TIMESTAMP)
    updated = db.Column(db.TIMESTAMP)


### File Objects
class TorrentFile(db.Model):
    __tablename__ = 'torrent_file'

    id = db.Column(db.Integer, primary_key=True)

    collection_id = db.Column(db.Integer, db.ForeignKey('torrent_file_collection.id'))
    collection = db.relationship(TorrentFileCollection, primaryjoin=collection_id == TorrentFileCollection.id)

    torrent_id = db.Column(db.Integer, db.ForeignKey('torrent.id'))
    torrent = db.relationship(Torrent, primaryjoin=torrent_id == Torrent.id)

    size = db.Column(db.Integer)
    rel_path = db.Column(db.Text)
    info_hash = db.Column(db.String(length=40))


class MediaFile(db.Model):
    __tablename__ = 'media_file'

    id = db.Column(db.Integer, primary_key=True)

    collection_id = db.Column(db.Integer, db.ForeignKey('media_file_collection.id'))
    collection = db.relationship(MediaFileCollection, primaryjoin=collection_id == MediaFileCollection.id)

    song_id = db.Column(db.Integer, db.ForeignKey('song.id'))
    song = db.relationship(Song, primaryjoin=song_id == Song.id)

    torrent_file_id = db.Column(db.Integer, db.ForeignKey('torrent_file.id'))
    torrent_file = db.relationship(TorrentFile, primaryjoin=torrent_file_id == TorrentFile.id)

    size = db.Column(db.Integer)
    rel_path = db.Column(db.Text)
    mime_type = db.Column(db.Text)
    sha256 = db.Column(db.String(length=64))

