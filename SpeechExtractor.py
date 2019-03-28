import threading


class SpeechExtractor(threading.Thread):
    def __init__(self, queue, cache_dict):
        threading.Thread.__init__(self, args=(), kwargs=None)
        self.cache_dict = cache_dict
        self.queue = queue

    def run(self):
        print(threading.currentThread().getName())
        while True:
            self.queue.put("Send Message to Text Extractor")
            self.cache_dict["raw_text"] = "GAL BRAUNNN"
