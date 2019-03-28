import time
from utils import Worker


class SpeechExtractor(Worker):
    def _step(self):
        self.queue.put("Send Message to Text Extractor")
        self.cache_dict["raw_text"] = "GAL BRAUNNN" + str(time.time())
