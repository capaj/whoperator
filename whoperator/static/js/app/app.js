(function(angular) {
    'use strict';
    var app = angular.module('whoperator', []);


    app.controller('AppCtrl', [function() {
        this.contextTemplate = 'static/js/app/main/main.html';

        this.mainTemplate = function() {
            this.contextTemplate = 'static/js/app/main/main.html';
        };

        this.generalSettings = function() {
            this.contextTemplate = 'static/js/app/settings/general.html';
        };

        this.apiSettings = function() {
            this.contextTemplate = 'static/js/app/settings/api.html';
        };

        this.cacheSettings = function() {
            this.contextTemplate = 'static/js/app/settings/cache.html';
        };

        this.rTorrentSettings = function() {
            this.contextTemplate = 'static/js/app/settings/rTorrent.html';
        };

        this.keyBindingsSettings = function() {
            this.contextTemplate = 'static/js/app/settings/keybindings.html';
        };
    }]);
})(angular);
