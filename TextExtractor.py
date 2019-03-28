import threading
import time


class TextExtractor(threading.Thread):
    def __init__(self, queue, cache_dict):
        threading.Thread.__init__(self, args=(), kwargs=None)
        self.queue = queue
        self.cache_dict = cache_dict

    def run(self):
        print(threading.currentThread().getName())
        while True:
            val = self.queue.get()
            self.action(val)
            time.sleep(0.01)

    def action(self, message):
        pass
