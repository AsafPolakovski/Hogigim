angular.module('hogigimApp', [])
    .controller('MainController', function($http, $interval) {
        var app = this;
        app.active = false;
        app.interval_promise = null;
        app.state = {};

        update_state = function(new_state) {
            app.state = Object.assign(app.state, new_state);
        };

        pool_state = function() {
            console.log("Polling...");
            $http.get('/status').then(
                function (result) {
                    console.log("poll success", result);
                    update_state(result.data);
                },
                function (result) {
                    console.log("poll failure", result);
                }
            )
        };

        app.cancel_session = function() {
            $http.get('/stop').then(
                function() {
                    console.log("Session stopped...");
                    $interval.cancel(app.interval_promise);
                    app.interval_promise = null;
                    app.active = false;
                },
                function(result) {
                    console.log("Session failed to end :(", result);
                }
            );
        };

        app.start_session = function () {
            $http.get('/start').then(
                function () {
                    console.log("Session started...");
                    app.state = Object.assign(app.state, {
                        'first_name': 'Kobe',
                        'last_name': 'Bryant',
                        'height': '1.98m',
                        'weight': '96kg',
                    });
                    app.interval_promise = $interval(pool_state, 1000);
                    app.active = true;
                },
                function (result) {
                    console.log("Session failed to start :(", result);
                }
            )
        };

        app.key_pressed = function (event) {
            if (event.key === "Enter") {
                if (app.active)  {
                    app.cancel_session();
                } else {
                    app.start_session();
                }
            }
            console.log("Key pressed:", event);
        };
    });
