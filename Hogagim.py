from queue import Queue

from SpeechExtractor import SpeechExtractor
from TextExtractor import TextExtractor
from flask import Flask

app = Flask(__name__)


def create_app():
    cache_dict = {}
    app = Flask(__name__)

    @app.route('/status')
    def get_status():
        return cache_dict.__str__()

    def create_extractors():
        q = Queue()
        speechExtractorThread = SpeechExtractor(q, cache_dict)
        textExtractorThread = TextExtractor(q, cache_dict)
        speechExtractorThread.start()
        textExtractorThread.start()

    # Initiate
        create_extractors()

    return app


if __name__ == '__main__':
    app = create_app()
    app.run()
