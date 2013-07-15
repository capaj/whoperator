(function(angular) {
    'use strict';
    var app = angular.module('whoperator');

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
