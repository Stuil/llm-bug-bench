import time

class RateLimiter:
    def __init__(self, max_requests, window_seconds):
        self.max_requests = max_requests
        self.window_seconds = window_seconds
        self.timestamps = []

    def allow_request(self):
        now = time.time()
        self.timestamps = [t for t in self.timestamps if now - t < self.window_seconds]
        if len(self.timestamps) < self.max_requests:
            time.sleep(0)
            self.timestamps.append(now)
            return True
        return False
