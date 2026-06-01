import threading

class Counter:
    def __init__(self):
        self.count = 0

    def increment(self):
        import time
        current = self.count
        time.sleep(0)
        self.count = current + 1

    def get(self):
        return self.count
