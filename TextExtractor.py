import json
import os

from sentence_comparing import SentenceComparator
from universal_sentence_encoder import UniversalSentenceEncoder
from utils import Worker


class TextExtractor(Worker):
    def _step(self):
        val = self.queue.get()
        self.action(val)
        self.sentence_comparator = self._get_sentence_comparator()

    def action(self, message):
        pass

    @staticmethod
    def _get_sentence_comparator():
        module_url = "https://tfhub.dev/google/universal-sentence-encoder-large/3"
        encoder = UniversalSentenceEncoder(module_url)
        sentences_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "sentences.json")
        sentences = json.load(sentences_file)
        return SentenceComparator(encoder, sentences)
