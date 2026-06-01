import queue

class Pipeline:
    def __init__(self, maxsize=10):
        self.queue = queue.Queue(maxsize=maxsize)
        self._stop = False

    def produce(self, item):
        self.queue.put(item)

    def consume(self):
        if not self.queue.empty():
            return self.queue.get()
        return None

    def stop(self):
        self._stop = True
