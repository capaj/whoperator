(function(angular) {
    'use strict';
    var app = angular.module('whoperator');

    app.controller('ManagementCtrl', [function() {
        this.curPage = 1;
        this.archiveSettingsOptions = {
            browseBy: ['Artist', 'Albums', 'Other'],
            resultsPerPage: [25, 50, 100],
            sortBy: ['Artist', 'Sync Date', null, 'Albums', 'Singles', 'EPs']
        };
        this.archiveSettings = {
            browseBy: 'Artist',
            resultsPerPage: 25,
            sortBy: 'Artist'
        };

        this.items = [
            {
                selected: false,
                artist: 'Warpaint',
                syncDate: 'May 1st, 2013'
            },
            {
                selected: false,
                artist: 'Warpaint',
                syncDate: 'May 1st, 2013'
            },
            {
                selected: false,
                artist: 'Warpaint',
                syncDate: 'May 1st, 2013'
            },
            {
                selected: false,
                artist: 'Warpaint',
                syncDate: 'May 1st, 2013'
            },
            {
                selected: false,
                artist: 'Warpaint',
                syncDate: 'May 1st, 2013'
            },
            {
                selected: false,
                artist: 'Warpaint',
                syncDate: 'May 1st, 2013'
            },
            {
                selected: false,
                artist: 'Warpaint',
                syncDate: 'May 1st, 2013'
            },
            {
                selected: false,
                artist: 'Warpaint',
                syncDate: 'May 1st, 2013'
            },
            {
                selected: false,
                artist: 'Warpaint',
                syncDate: 'May 1st, 2013'
            },
            {
                selected: false,
                artist: 'Warpaint',
                syncDate: 'May 1st, 2013'
            },
            {
                selected: false,
                artist: 'Warpaint',
                syncDate: 'May 1st, 2013'
            }
        ];

        this.pagination = function() {
            return _.range(1,
                Math.ceil(this.items.length / this.archiveSettings.resultsPerPage) + 1
            );
        }
    }]);
})(angular);
