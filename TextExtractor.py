from utils import Worker


class TextExtractor(Worker):
    def _step(self):
        val = self.queue.get()
        self.action(val)

    def action(self, message):
        pass
