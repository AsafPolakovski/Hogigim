from queue import Queue

from SpeechExtractor import SpeechExtractor
from TextExtractor import TextExtractor
from flask import Flask, jsonify
import atexit

app = Flask(__name__)


def create_app():
    cache_dict = {}
    app = Flask(__name__)

    def interrupt():
        global speech_extractor_thread
        global text_extractor_thread

        speech_extractor_thread.cancel()
        text_extractor_thread.cancel()

    @app.route('/')
    def root():
        return open('index.html', 'r').read()

    @app.route('/status')
    def get_status():
        return jsonify(cache_dict)

    def create_extractors():
        global speech_extractor_thread
        global text_extractor_thread
        q = Queue()
        speech_extractor_thread = SpeechExtractor(q, cache_dict)
        text_extractor_thread = TextExtractor(q, cache_dict)
        speech_extractor_thread.start()
        text_extractor_thread.start()

    # Initiate
    create_extractors()
    atexit.register(interrupt)


    return app


if __name__ == '__main__':
    app = create_app()
    app.run(host="0.0.0.0")
