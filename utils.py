import threading
import time


class Worker(threading.Thread):
    def __init__(self, queue, cache_dict, stop_event):
        super().__init__()
        self.queue = queue
        self.cache_dict = cache_dict
        self.stop_event = stop_event

    def run(self):
        print(threading.currentThread().getName())
        while not self.stop_event.isSet():
            self._step()
            time.sleep(0.01)

    def _step(self):
        pass
