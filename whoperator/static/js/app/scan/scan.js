(function(angular) {
    'use strict';
    var app = angular.module('whoperator');

    app.controller('ScanCtrl', [function() {
        this.tableTitles = ['Status', 'Torrent', 'Scan Time'];
        this.scanItems = [
            {
                status: 'Verified',
			    torrent: 'Atlas Sound - Axis Tour CD-R - 2006 (CD - MP3 - V0 (VBR)).torrent',
			    scanTime: '2013-07-01 23:37:26'
            },
            {
                status: 'Verified',
                torrent: 'Atlas Sound - Fractal Trax - 2006 (CD - MP3 - 320).torrent',
                scanTime: '2013-07-01 23:37:26'
            },
            {
                status: 'Verified',
                torrent: 'Atlas Sound - Fractal Trax - 2006 (CD - MP3 - 320).torrent',
                scanTime: '2013-07-01 23:37:26',
                error: true
            },
            {
                status: 'Verified',
                torrent: 'Atlas Sound - Fractal Trax - 2006 (CD - MP3 - 320).torrent',
                scanTime: '2013-07-01 23:37:26'
            },
            {
                status: 'Verified',
                torrent: 'Atlas Sound - Fractal Trax - 2006 (CD - MP3 - 320).torrent',
                scanTime: '2013-07-01 23:37:26',
                error: true
            },
            {
                status: 'Verified',
                torrent: 'Atlas Sound - Fractal Trax - 2006 (CD - MP3 - 320).torrent',
                scanTime: '2013-07-01 23:37:26'
            },
            {
                status: 'Verified',
                torrent: 'Atlas Sound - Fractal Trax - 2006 (CD - MP3 - 320).torrent',
                scanTime: '2013-07-01 23:37:26'
            },
            {
                status: 'Verified',
                torrent: 'Atlas Sound - Fractal Trax - 2006 (CD - MP3 - 320).torrent',
                scanTime: '2013-07-01 23:37:26'
            },
            {
                status: 'Verified',
                torrent: 'Atlas Sound - Fractal Trax - 2006 (CD - MP3 - 320).torrent',
                scanTime: '2013-07-01 23:37:26'
            },
            {
                status: 'Verified',
                torrent: 'Atlas Sound - Fractal Trax - 2006 (CD - MP3 - 320).torrent',
                scanTime: '2013-07-01 23:37:26'
            },
            {
                status: 'Verified',
                torrent: 'Atlas Sound - Fractal Trax - 2006 (CD - MP3 - 320).torrent',
                scanTime: '2013-07-01 23:37:26'
            },
            {
                status: 'Verified',
                torrent: 'Atlas Sound - Fractal Trax - 2006 (CD - MP3 - 320).torrent',
                scanTime: '2013-07-01 23:37:26'
            },
            {
                status: 'Verified',
                torrent: 'Atlas Sound - Fractal Trax - 2006 (CD - MP3 - 320).torrent',
                scanTime: '2013-07-01 23:37:26'
            }
        ];
    }]);
})(angular);
