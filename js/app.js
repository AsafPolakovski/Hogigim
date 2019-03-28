angular.module('hogigimApp', [])
    .controller('MainController', function($http, $interval) {
        var app = this;
        app.state = {
            'first_name': 'Kobe',
            'last_name': 'Bryant',
            'height': '1.98m',
        }
    });