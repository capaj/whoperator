(function(angular) {
    'use strict';
    var app = angular.module('whoperator');

    app.controller('DashboardCtrl', [function() {
        this.stats = [
            { label: 'Artists', data: 344 },
            { label: 'Torrents', data: 4283 },
            { label: 'Albums', data: 788 },
            { label: 'Singles', data: 510 },
            { label: 'Queue', data: 510 },
            { label: 'Last Global Sync', data: 'Tuesday, July 3rd, 2012' }
        ];
    }]);
})(angular);
