'use strict';

module.exports = function(grunt) {
    grunt.initConfig({
        jshint: {
            all: [
                'Gruntfile.js',
                'whoperator/static/js/app/*.js'
            ],
            options: {
                jshintrc: '.jshintrc'
            }
        },
        watch: {
            all: {
                files: ['<%= jshint.all %>'],
                tasks: ['jshint:all'],
                options: {
                    interrupt: true
                }
            }
        }
    });
    grunt.loadNpmTasks('grunt-contrib-watch');
    grunt.loadNpmTasks('grunt-contrib-jshint');

    grunt.registerTask('hint', ['watch:all']);
};
