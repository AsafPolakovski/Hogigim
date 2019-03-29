from queue import Queue
from threading import Event

from SpeechExtractor import SpeechExtractor, GoogleHandler
from TextExtractor import TextExtractor
from ConsoleText import ConsoleReader
from flask import Flask, jsonify, request

import logging
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

app = Flask(__name__)
SPEECH_THREADS = [SpeechExtractor, GoogleHandler]

USERS = {
    1: {
        'first_name': 'Kobe',
        'last_name': 'Bryant',
        'height': '1.98m',
        'weight': '96kg',
    },
    2: {
        'first_name': 'Asaf',
        'last_name': 'Polakovsy',
        'height': None,
        'weight': None,
    },
    3: {
        'first_name': 'Sharon',
        'last_name': 'Yogev',
        'height': '1.89m',
        'weight': '90kg',
    },
    4: {
        'first_name': 'Or',
        'last_name': 'Troyaner',
        'height': None,
        'weight': None,
    },
    5: {
        'first_name': 'Gal',
        'last_name': 'Braun',
        'height': None,
        'weight': None,
    },
    6: {
        'first_name': 'Ron',
        'last_name': 'Likovnik',
        'height': None,
        'weight': None,
    },
}


def create_app():
    cache_dict = {}
    app = Flask(__name__)
    q = Queue()
    speech_queue = Queue()
    stop_event = Event()
    threads = []

    @app.route('/')
    def root():
        return open('index.html', 'r').read()

    @app.route('/status')
    def get_status():
        #print(cache_dict.__str__())
        return jsonify(cache_dict)

    @app.route('/start')
    def start_threads():
        user_id = int(request.args.get('user_id', '1'))
        new_threads = [T(q, cache_dict, stop_event, speech_queue) for T in SPEECH_THREADS]
        new_threads.append(TextExtractor(q, cache_dict, stop_event))
        new_threads.append(ConsoleReader(q, cache_dict, stop_event))
        for t in new_threads:
            t.start()
        threads.extend(new_threads)
        cache_dict.update(USERS[user_id])
        return jsonify({'success': True})

    @app.route('/stop')
    def stop_threads():
        stop_event.set()
        for t in threads:
            t.join()
        threads.clear()
        stop_event.clear()
        return jsonify({'success': True})

    def _app_stop():
        stop_event.set()
        for thread in threads:
            thread.join()

    return app, _app_stop


if __name__ == '__main__':
    app, stop = create_app()
    app.run(host="0.0.0.0")
    print('stopping...')
    stop()
