from utils import Worker


class ConsoleReader(Worker):
    def __init__(self, queue, cache_dict, stop_event):
        self.speaker = 'Doctor'
        super().__init__(queue, cache_dict, stop_event)
        self.cache_dict["transcript"] = ""  # setup transcript
        print('WHAT!!!')

    def _step(self):
        try:
            text = input('{}:'.format(self.speaker))
            print("speech", self.speaker, text)
            self.queue.put((self.speaker, text))
            self.cache_dict["transcript"] += "{}: {}\n".format(self.speaker, text)
            if self.speaker == 'Doctor':
                self.speaker = 'Patient'
            else:
                self.speaker = 'Doctor'
        except Exception as e:
            self.queue.put(('exception', str(e)))
