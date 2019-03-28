from queue import Queue
from threading import Event

from SpeechExtractor import SpeechExtractor
from TextExtractor import TextExtractor
from flask import Flask, jsonify
import atexit

app = Flask(__name__)
THREADS = [SpeechExtractor, TextExtractor]


def create_app(stop_event):
    cache_dict = {}
    app = Flask(__name__)

    @app.route('/')
    def root():
        return open('index.html', 'r').read()

    @app.route('/status')
    def get_status():
        return jsonify(cache_dict)

    def create_extractors():
        q = Queue()
        threads = [T(q, cache_dict, stop_event) for T in THREADS]
        for t in threads:
            t.start()
        return threads

    # Initiate
    threads = create_extractors()

    return app, threads


if __name__ == '__main__':
    stop_event = Event();
    app, threads = create_app(stop_event)
    app.run(host="0.0.0.0")
    print('stopping...')
    stop_event.set()
    for thread in threads:
        thread.join()
