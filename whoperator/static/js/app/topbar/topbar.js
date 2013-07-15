(function(angular) {
    'use strict';
    var app = angular.module('whoperator');
    
    app.controller('TopbarCtrl', ['TrackService', function(TrackService) {
        var self = this;
        this.tracks = null;
        
        TrackService.get().then(function(tracks) {
            self.tracks = tracks;
        });
    }]);
})(angular);
