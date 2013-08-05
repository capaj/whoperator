(function(angular) {
    'use strict';
    var app = angular.module('whoperator');

    app.factory('TemplateService', function() {
        var _primarySettings = [
            { label: 'Main', path: 'static/js/app/main/main.html' },
            { label: 'General', path: 'static/js/app/settings/general.html' },
            { label: 'API', path: 'static/js/app/settings/api.html' },
            { label: 'Cache', path: 'static/js/app/settings/cache.html' },
            { label: 'Key Bindings', path: 'static/js/app/settings/keybindings.html' }
        ];

        var _pluginSettings = [
            { label: 'rTorrent', path: 'static/js/app/settings/rTorrent.html' }
        ];

        return {
            primarySettings: _primarySettings,
            pluginSettings: _pluginSettings
        };
    });

    app.factory('TrackService', ['$q', function($q) {
        return {
            get: function() {
                var defer = $q.defer();
                var data = [
                    {
                        artist: 'Strokes',
                        album: 'Is This It',
                        title: '1. Is This It',
                        length: '2:34'
                    },
                    {
                        artist: 'Strokes',
                        album: 'Is This It',
                        title: '1. Is This It',
                        length: '2:34'
                    },
                    {
                        artist: 'Strokes',
                        album: 'Is This It',
                        title: '1. Is This It',
                        length: '2:34'
                    },
                    {
                        artist: 'Strokes',
                        album: 'Is This It',
                        title: '1. Is This It',
                        length: '2:34'
                    },
                    {
                        artist: 'Strokes',
                        album: 'Is This It',
                        title: '1. Is This It',
                        length: '2:34'
                    },
                    {
                        artist: 'Strokes',
                        album: 'Is This It',
                        title: '1. Is This It',
                        length: '2:34'
                    },
                    {
                        artist: 'Strokes',
                        album: 'Is This It',
                        title: '1. Is This It',
                        length: '2:34'
                    },
                    {
                        artist: 'Strokes',
                        album: 'Is This It',
                        title: '1. Is This It',
                        length: '2:34'
                    },
                    {
                        artist: 'Strokes',
                        album: 'Is This It',
                        title: '1. Is This It',
                        length: '2:34'
                    },
                    {
                        artist: 'Strokes',
                        album: 'Is This It',
                        title: '1. Is This It',
                        length: '2:34'
                    },
                    {
                        artist: 'Strokes',
                        album: 'Is This It',
                        title: '1. Is This It',
                        length: '2:34'
                    },
                    {
                        artist: 'Strokes',
                        album: 'Is This It',
                        title: '1. Is This It',
                        length: '2:34'
                    }
                ];
                defer.resolve(data);
                return defer.promise;
            }
        };
    }]);
})(angular);
