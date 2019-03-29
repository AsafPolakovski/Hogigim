import numpy as np
from sklearn.metrics.pairwise import cosine_similarity


class SentenceComparator:
    def __init__(self, sentences, encoder, threshold=0.5):
        self.encoder = encoder
        self.sentence_vectors_list = encoder.encode(sentences)
        self.sentences = sentences
        self.threshold = threshold

    def get_most_similar(self, input_sentence):
        input_sentence_vec = self.encoder.encode(input_sentence).reshape(-1)
        distances = cosine_similarity(input_sentence_vec, self.sentence_vectors_list)
        max_index = np.argmax(distances)
        max_value = distances[max_index]
        if max_value < self.threshold:
            return None
        return self.sentences[max_index]
