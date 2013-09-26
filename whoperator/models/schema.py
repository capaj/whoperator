from datetime import datetime
from pygazelle import media, format, encoding
from sqlalchemy import Table
from sqlalchemy.ext.associationproxy import association_proxy

from whoperator import db


### What.cd Objects

class ArtistAppearance(db.Model):
    __tablename__ = 'artist_appearance'

    artist_id = db.Column(db.Integer, db.ForeignKey('artist.id'), primary_key=True)
    torrent_group_id = db.Column(db.Integer, db.ForeignKey('torrent_group.id'), primary_key=True)

    artist = db.relationship("Artist", primaryjoin="ArtistAppearance.artist_id == Artist.id",
                             backref=db.backref("torrent_groups", cascade="all, delete-orphan"))
    
    torrent_group = db.relationship("TorrentGroup", primaryjoin="ArtistAppearance.torrent_group_id == TorrentGroup.id",
                                    backref=db.backref("artists", cascade="all, delete-orphan"))


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

    torrent_groups = association_proxy("torrent_groups", "torrent_group",
                                       creator=lambda torrent_group: ArtistAppearance(torrent_group=torrent_group))

    def __init__(self, what_artist=None):
        self.created = self.updated = datetime.now()
        if what_artist is not None:
            self.update_from_what(what_artist)

    def update_from_what(self, what_artist):
        if self.what_id and self.what_id != what_artist.id:
            raise Exception("Tried to update Artist id %s with data from id %s" % (self.id, what_artist.id))

        self.what_id = what_artist.id
        self.name = what_artist.name
        self.image = what_artist.image
        self.body = what_artist.body
        self.vanity_house = what_artist.vanity_house
        self.updated = datetime.now()

    def as_dict(self):
        return dict([(c.name, getattr(self, c.name)) for c in self.__table__.columns])


class TorrentGroup(db.Model):
    __tablename__ = 'torrent_group'

    id = db.Column(db.Integer, primary_key=True)

    what_id = db.Column(db.Integer, index=True)
    name = db.Column(db.String(length=255))

    artists = association_proxy("artists", "artist",
                                   creator=lambda artist: ArtistAppearance(artist=artist))

    wiki_body = db.Column(db.Text)
    wiki_image = db.Column(db.Text)
    year = db.Column(db.Integer)
    record_label = db.Column(db.String(length=100))
    catalogue_number = db.Column(db.String(length=100))
    vanity_house = db.Column(db.Boolean)
    time = db.Column(db.DATETIME)

    created = db.Column(db.TIMESTAMP)
    updated = db.Column(db.TIMESTAMP)

    def __init__(self, what_torrentgroup=None):
        self.created = self.updated = datetime.now()
        if what_torrentgroup is not None:
            self.update_from_what(what_torrentgroup)

    def update_from_what(self, what_torrentgroup):
        if self.what_id and self.what_id != what_torrentgroup.id:
            raise Exception("Tried to update Album (TorrentGroup) id %s with data from id %s" % (self.id, what_torrentgroup.id))

        self.what_id = what_torrentgroup.id
        self.name = what_torrentgroup.name
        self.wiki_body = what_torrentgroup.wiki_body
        self.wiki_image = what_torrentgroup.wiki_image
        self.year = what_torrentgroup.year
        self.record_label = what_torrentgroup.record_label
        self.catalogue_number = what_torrentgroup.catalogue_number
        self.vanity_house = what_torrentgroup.vanity_house
        self.time = what_torrentgroup.time

        self.updated = datetime.now()

    def as_dict(self):
        return dict([(c.name, getattr(self, c.name)) for c in self.__table__.columns])


class Torrent(db.Model):
    __tablename__ = 'torrent'

    id = db.Column(db.Integer, primary_key=True)

    # use db id, not what_id
    torrent_group_id = db.Column(db.Integer, db.ForeignKey('torrent_group.id'))
    torrent_group = db.relationship(TorrentGroup, primaryjoin="Torrent.torrent_group_id == TorrentGroup.id",
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
        self.created = self.updated = datetime.now()

        # TODO: make update optional so that we can create without pulling from what
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

    def as_dict(self):
        return dict([(c.name, getattr(self, c.name)) for c in self.__table__.columns])


class Song(db.Model):
    __tablename__ = 'song'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(length=255))

    # use db id, not what_id
    artist_id = db.Column(db.Integer, db.ForeignKey('artist.id'))
    artist = db.relationship(Artist, primaryjoin="Song.artist_id == Artist.id",
                             backref=db.backref("songs", cascade="all,delete"))

    torrent_group_id = db.Column(db.Integer, db.ForeignKey('torrent_group.id'))
    torrent_group = db.relationship(TorrentGroup, primaryjoin="Song.torrent_group_id == TorrentGroup.id",
                                    backref=db.backref("songs", cascade="all,delete"))

    def __init__(self, name, artist_id, torrent_group_id):
        self.name = name
        self.artist_id = artist_id
        self.torrent_group_id = torrent_group_id


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

    def as_dict(self):
        return dict([(c.name, getattr(self, c.name)) for c in self.__table__.columns])


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

    def as_dict(self):
        return dict([(c.name, getattr(self, c.name)) for c in self.__table__.columns])


### File Objects
class TorrentFile(db.Model):
    __tablename__ = 'torrent_file'

    id = db.Column(db.Integer, primary_key=True)

    collection_id = db.Column(db.Integer, db.ForeignKey('torrent_file_collection.id'))
    collection = db.relationship(TorrentFileCollection, primaryjoin="TorrentFile.collection_id == TorrentFileCollection.id",
                                 backref=db.backref("torrent_files", cascade="all,delete"))

    torrent_id = db.Column(db.Integer, db.ForeignKey('torrent.id'))
    torrent = db.relationship(Torrent, primaryjoin="TorrentFile.torrent_id == Torrent.id")

    size = db.Column(db.Integer)
    rel_path = db.Column(db.Text)
    info_hash = db.Column(db.String(length=40), index=True)

    def __init__(self, collection_id, torrent_id, size, rel_path, info_hash, context=None):
        self.collection_id = collection_id
        self.torrent_id = torrent_id
        self.size = size
        self.rel_path = rel_path
        self.info_hash = info_hash

    def as_dict(self):
        return dict([(c.name, getattr(self, c.name)) for c in self.__table__.columns])


class MediaFile(db.Model):
    __tablename__ = 'media_file'

    id = db.Column(db.Integer, primary_key=True)

    collection_id = db.Column(db.Integer, db.ForeignKey('media_file_collection.id'))
    collection = db.relationship(MediaFileCollection, primaryjoin="MediaFile.collection_id == MediaFileCollection.id",
                                 backref=db.backref("media_files", cascade="all,delete"))

    song_id = db.Column(db.Integer, db.ForeignKey('song.id'))
    song = db.relationship(Song, primaryjoin="MediaFile.song_id == Song.id")

    torrent_file_id = db.Column(db.Integer, db.ForeignKey('torrent_file.id'))
    torrent_file = db.relationship(TorrentFile, primaryjoin="MediaFile.torrent_file_id == TorrentFile.id")

    size = db.Column(db.Integer)
    rel_path = db.Column(db.Text)
    mime_type = db.Column(db.Text)
    sha256 = db.Column(db.String(length=64))

    def __init__(self, collection_id, song_id, torrent_file_id, size, rel_path, mime_type, sha256):
        self.collection_id = collection_id
        self.song_id = song_id
        self.torrent_file_id = torrent_file_id
        self.size = size
        self.rel_path = rel_path
        self.mime_type = mime_type
        self.sha256 = sha256

    def as_dict(self):
        return dict([(c.name, getattr(self, c.name)) for c in self.__table__.columns])
