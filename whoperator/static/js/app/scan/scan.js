(function(angular, _) {
    'use strict';
    var app = angular.module('whoperator');

    app.controller('ScanCtrl', ['TorrentFileCollectionService', 'TorrentFileService',
        function(TorrentFileCollectionService, TorrentFileService) {
            this.tableTitles = ['Status', 'Torrent ID', 'Torrent', 'Info Hash', 'Updated'];
            this.torrentFileCollections = TorrentFileCollectionService.get();
            this.torrentFileItems = TorrentFileService.get();
    }]);

    app.factory('TorrentFileCollectionService', ['$http', function($http) {
        return {
          get: function() {
            return $http.get('/torrent_collection/1').then(function(result) {
                var keys = [];
                for (var key in result.data) {
                  if (result.data.hasOwnProperty(key)) {
                    keys.push(key);
                  }
                }

                return keys.map(function(key) {
                    return new TorrentFileCollectionItem(result.data[key]);
                });
            });
          }
        }
    }]);

    app.factory('TorrentFileService', ['$http', function($http) {
        return {
          get: function() {
            return $http.get('/torrent_collection/1/item').then(function(result) {
                return _.map(result.data.items, function(item) {
                    return new TorrentFileItem(_.extend(item, { updated: result.data.items.updated }));
                });
            });
          }
        }
    }]);

    function TorrentFileCollectionItem(data) {
        this.id = data.id;
        this.name = data.name;
        this.path = data.path;
        this.recurse = data.recurse;
        this.updated = moment(data.updated).fromNow();
    }

    function TorrentFileItem(data) {
        this.torrentId = data.torrent_id;
        // mark as error if torrent_id is -1
        this.error = !~data.torrent_id;
        this.status = this.error ? 'invalid' : 'verified';
        this.torrent = data.rel_path;
        this.infoHash = data.info_hash;
    }
})(angular, _);
