(function(angular, Mousetrap) {
    'use strict';
    var app = angular.module('whoperator');

    app.factory('KeyBindingsService', ['$q', function($q) {
        var keyBindings = [
            new KeyBinding('Play/Pause', 'gp'),
            new KeyBinding('Stop', 'gs'),
            new KeyBinding('Next Track', 'g>'),
            new KeyBinding('Previous Track', 'g<'),
            new KeyBinding('Search', 'g/'),
            new KeyBinding('Show Log', 'gl'),
            new KeyBinding('Volume Up', 'gu'),
            new KeyBinding('Volume Down', 'gd'),
            new KeyBinding('Unused', ''),
            new KeyBinding('Unused', ''),
            new KeyBinding('Unused', ''),
            new KeyBinding('Unused', ''),
            new KeyBinding('Unused', ''),
            new KeyBinding('Unused', ''),
            new KeyBinding('Unused', ''),
            new KeyBinding('Unused', ''),
            new KeyBinding('Unused', ''),
            new KeyBinding('Unused', ''),
            new KeyBinding('Unused', ''),
            new KeyBinding('Unused', '')
        ];

        function _bindKeys(keyBindings) {
            _.each(keyBindings, function(keyBinding) {
                var binding = keyBinding.binding;
                binding = binding.split('').join(' ');
                console.log(binding);
                Mousetrap.bind(binding, function() {
                    console.log('binding for', keyBinding.label);
                });
            });
        }

        var defer = $q.defer();
        defer.resolve(keyBindings);
        defer.promise.then(function(keyBindings) {
            _bindKeys(keyBindings);
        });
        return {
            get: function(id) {
                return defer.promise;
            }
        };
    }]);

    function KeyBinding(label, binding) {
        this.label = label;
        this.binding = binding;
    }
})(angular, Mousetrap);
