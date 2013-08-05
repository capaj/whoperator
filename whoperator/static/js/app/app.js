(function(angular) {
    'use strict';
    var app = angular.module('whoperator', []);

    app.controller('AppCtrl', ['PlayerService', 'TemplateService',
        function(PlayerService, TemplateService) {
            this.contextTemplate = TemplateService.primarySettings[0].path;

            this.primarySettings = TemplateService.primarySettings;
            this.pluginSettings = TemplateService.pluginSettings;

            this.setTemplate = function(templatePath) {
                this.contextTemplate = templatePath;
            };
        }
    ]);
})(angular);
