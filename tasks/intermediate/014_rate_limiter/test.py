import threading
from buggy import RateLimiter

def test_within_limit():
    limiter = RateLimiter(3, 10)
    assert limiter.allow_request() is True
    assert limiter.allow_request() is True
    assert limiter.allow_request() is True

def test_exceed_limit():
    limiter = RateLimiter(2, 10)
    limiter.allow_request()
    limiter.allow_request()
    assert limiter.allow_request() is False

def test_concurrent():
    limiter = RateLimiter(5, 10)
    results = []
    lock = threading.Lock()
    barrier = threading.Barrier(20)
    def req():
        barrier.wait()
        allowed = limiter.allow_request()
        with lock:
            results.append(allowed)
    threads = [threading.Thread(target=req) for _ in range(20)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()
    allowed_count = sum(1 for r in results if r)
    assert allowed_count <= 5, f"Allowed {allowed_count}, max is 5"
