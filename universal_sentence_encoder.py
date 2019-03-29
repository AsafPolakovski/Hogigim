import tensorflow as tf
import tensorflow_hub as hub


class UniversalSentenceEncoder:
    def __init__(self, module_url):
        self.embed = hub.Module(module_url)
        self.session = tf.Session()
        self.session.run([tf.global_variables_initializer(), tf.tables_initializer()])

    def encode(self, sentences):
        if type(sentences) == str:
            sentences = [sentences]

        return self.session.run(self.embed(sentences))
