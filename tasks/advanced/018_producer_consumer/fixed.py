import queue

class Pipeline:
    def __init__(self, maxsize=10):
        self.queue = queue.Queue(maxsize=maxsize)

    def produce(self, item):
        self.queue.put(item)

    def consume(self, timeout=0.1):
        try:
            return self.queue.get(timeout=timeout)
        except queue.Empty:
            return None
