import threading
from buggy import Counter

def test_single_thread():
    c = Counter()
    c.increment()
    c.increment()
    assert c.get() == 2

def test_multi_thread():
    c = Counter()
    n = 100
    threads = []
    barrier = threading.Barrier(10)
    def work():
        barrier.wait()
        for _ in range(n):
            c.increment()
    for _ in range(10):
        t = threading.Thread(target=work)
        threads.append(t)
        t.start()
    for t in threads:
        t.join()
    assert c.get() == n * 10, f"Expected {n * 10}, got {c.get()}"
