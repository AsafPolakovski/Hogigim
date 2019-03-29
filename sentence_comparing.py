class SentenceComparator:
    def __init__(self, sentences, encoder):
        self.encoder = encoder
        self.sentence_vectors_list = encoder.encode(sentences)
        self.sentences = sentences

    def get_most_similar(self, sentence):
        sentence_vec = self.encoder.encode(sentence)
