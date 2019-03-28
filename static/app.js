angular.module('hogigimApp', [])
    .controller('MainController', function($http, $interval) {
        var app = this;
        app.active = false;
        app.interval_promise = null;
        app.state = {};

        pool_state = function() {
            console.log("Polling...");
        }

        app.cancel_session = function() {
            console.log("Session stopped...");
            $interval.cancel(app.interval_promise);
            app.interval_promise = null;
            app.active = false;
        }

        app.start_session = function () {
            console.log("Session started...");
            app.state = Object.assign(app.state, {
                'first_name': 'Kobe',
                'last_name': 'Bryant',
                'height': '1.98m',
                'weight': '96kg',
            })
            app.interval_promise = $interval(pool_state, 1000);
            app.active = true;
        }

        app.key_pressed = function (event) {
            if (event.key == "Enter") {
                if (app.active)  {
                    app.cancel_session();
                } else {
                    app.start_session();
                }
            }
            console.log(event);
        };
    });
