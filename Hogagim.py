from queue import Queue

from SpeechExtractor import SpeechExtractor
from TextExtractor import TextExtractor
from flask import Flask
from flask import render_template
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
    def index_html():
        return render_template('index.html')

    @app.route('/status')
    def get_status():
        return cache_dict.__str__()

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
    app.run()
