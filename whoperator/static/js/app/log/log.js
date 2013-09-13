(function(angular, _) {
    'use strict';
    var app = angular.module('whoperator');

    app.controller('LogCtrl', ['LogService', function(LogService) {
            this.logItems = LogService.get();
    }]);

    app.factory('LogService', ['$http', function($http) {
        return {
          get: function() {
            return $http.get('/log').then(function(result) {
                return _.map(result.data.json_log, function(item) {
                    return new LogItem(item);
                });
            });
          }
        }
    }]);

    function LogItem(data) {
        this.id = data.id;
        this.date = data.date;
        this.level = data.level;
        this.text = data.text;
        this.type = data.type;
    }

})(angular, _);
