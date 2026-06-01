import time
import threading

class RateLimiter:
    def __init__(self, max_requests, window_seconds):
        self.max_requests = max_requests
        self.window_seconds = window_seconds
        self.timestamps = []
        self._lock = threading.Lock()

    def allow_request(self):
        with self._lock:
            now = time.time()
            self.timestamps = [t for t in self.timestamps if now - t < self.window_seconds]
            if len(self.timestamps) < self.max_requests:
                self.timestamps.append(now)
                return True
            return False
