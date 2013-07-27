(function(angular, _) {
    'use strict';
    var app = angular.module('whoperator');

    app.controller('SettingsCtrl', [function() {
    }]);

    app.controller('KeyBindingsCtrl', ['KeyBindingsService', function(KeyBindingsService) {
        var self = this;

        var keyBindings = KeyBindingsService.get().then(function(keyBindings) {
            var maxRowPerColumn = 10;
            var numOfColumns = Math.ceil(keyBindings.length / maxRowPerColumn);
            var columns = [];

            _.each(_.range(numOfColumns), function(columnNum) {
                columns.push(keyBindings.slice(
                    maxRowPerColumn * columnNum,
                    (columnNum + 1) === numOfColumns
                        ? keyBindings.length
                        : (columnNum * 10) + 10
                ));
            });

            self.keyBindingColumns = columns;
        });
    }]);
})(angular, _);
