(function(angular, _) {
    'use strict';
    var app = angular.module('whoperator');

    app.controller('ScanCtrl', ['ScanService', function(ScanService) {
        this.tableTitles = ['Status', 'Torrent ID', 'Torrent', 'Info Hash', 'Updated Time'];
        this.scanItems = ScanService.get();
    }]);

    app.factory('ScanService', ['$http', function($http) {
        return {
          get: function() {
            return $http.get('/torrent_collection/1/item').then(function(result) {
                return _.map(result.data.items, function(item) {
                    return new ScanItem(_.extend(item, { updated: result.data.items.updated }));
                });
            });
          }
        }
    }]);

    function ScanItem(data) {
        this.torrentId = data.torrent_id;
        // mark as error if collection_id is -1
        this.error = !~data.torrent_id;
        this.status = this.error ? 'invalid' : 'verified';
        this.torrent = data.rel_path;
        this.infoHash = data.info_hash;
        this.updated = data.updated;
    }
})(angular, _);
