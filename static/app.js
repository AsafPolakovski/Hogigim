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

        var canvas = document.querySelector('canvas'),
    ctx = canvas.getContext('2d'),
    lines = [],
    width = document.documentElement.clientWidth,
    height = document.documentElement.clientHeight,
    sequence = 0,
    frequency = 5,
    speed = .01,
    speedModifier = { s: 0 },
    speedTween = new TWEEN.Tween(speedModifier),
    amplitude = 20,
    ampModifier = { a: 0 },
    ampTween = new TWEEN.Tween(ampModifier);

canvas.width = width;
canvas.height = height;
ctx.imageSmoothingEnabled = true;
ctx.translate(0.5, 0.5);

ampTween
  .to({ a: 10 }, 4000)
  .repeat(Infinity)
  .yoyo(true)
  .easing(TWEEN.Easing.Cubic.InOut)
  .start()


///////////
//
// Line class
// Manages properties for individual lines
//
///////////

class Line {
  constructor (opts) {
    this.ctx = opts.ctx;
    this.amplitude = opts.amplitude || 20;
    this.frequency = opts.frequency || 5;
    this.sequence = 0;
    this.layer = opts.layer; // used to adjust opacity and fade lines
  }

  draw() {
    this.ctx.beginPath();
    this.ctx.lineWidth = 3;
    this.ctx.strokeStyle = 'rgba(100, 255, 255, ' + 1 / this.layer + ')';

    this.ctx.moveTo(0, height / 2);

    for (var i = 0; i < width; i++) {
      this.ctx.lineTo(i, this._getYPos(i, sequence))
    }

    this.ctx.stroke()
  }

  // calculate y-position for a given time and x-position
  _getYPos(xPos, sequence) {
    return ((this.amplitude + ampModifier.a) * Math.sin(Math.PI * (xPos / width) * this.frequency + -sequence)) * this._equalize(xPos) + height / 2;
  }

  // limits y position so wave starts and ends at 0
  _equalize(x) {
    let half = width / 2;

    return -Math.pow(1 / half * (x - half), 2) + 1;
  }
}


///////////
//
// Create lines
// Vary amps so we can space out the lines a little bit
//
///////////

let amps = [100, 80, 60, 40, 20];
amps.forEach((amp, i) => {
  let line = new Line({
    ctx: ctx,
    frequency: frequency,
    amplitude: amp,
    layer: i + 1
  });

  lines.push(line);
})


///////////
//
// Draw/animate the lines
//
///////////

let draw = () => {
  requestAnimationFrame(draw);
  TWEEN.update();

  ctx.clearRect(0, 0, width, height);

  for (var i = 0; i < lines.length; i ++) {
    lines[i].draw();
  }

  sequence += speed + speedModifier.s;
}

draw();


/////////////
//
// Resize if window changes or device rotates.
//
/////////////

window.addEventListener('resize', () => {
  ctx.clearRect(0, 0, width, height);

  width = window.innerWidth;
  height = window.innerHeight;

  canvas.width = width;
  canvas.height = height;
})


///////////
//
// Microphone stuff.
//
///////////

window.AudioContext = window.AudioContext || window.webkitAudioContext;
navigator.getUserMedia = navigator.webkitGetUserMedia || navigator.mozGetUserMedia;

var context = new AudioContext();
if (context.state !== 'running') {
    context.resume().then(() => {
    console.log('Playback resumed successfully');
  });
  }

var source,
    audioContext = new AudioContext(),
    processingNode = audioContext.createScriptProcessor(1024, 1, 1),
    maxLevel = 0,
    oldLevel = 0;

if (navigator.getUserMedia) {
  navigator.getUserMedia(
    { audio: true },
    function (stream) {
      source = audioContext.createMediaStreamSource(stream);
      source.connect(processingNode);
      processingNode.connect(audioContext.destination);
      processingNode.onaudioprocess = function(event){

        var input = event.inputBuffer.getChannelData(0),
            sum = 0;

        for(var i = 0; i < input.length; ++i) {
          sum += input[i] * input[i];
        }

        speedTween.stop().to({ s: sum / 80 }, 400).start()
      }
    },
    function(){}
  );
}


    });
