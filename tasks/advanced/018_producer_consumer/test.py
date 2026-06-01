import threading
import time
from buggy import Pipeline

def test_single_item():
    p = Pipeline()
    p.produce(42)
    assert p.consume() == 42

def test_multiple_items():
    p = Pipeline()
    for i in range(5):
        p.produce(i)
    for i in range(5):
        assert p.consume() == i

def test_consume_from_empty():
    p = Pipeline()
    result = p.consume()
    assert result is None

def test_concurrent():
    p = Pipeline(maxsize=5)
    results = []
    barrier = threading.Barrier(2)
    def producer():
        for i in range(20):
            p.produce(i)
            time.sleep(0.01)
    def consumer():
        barrier.wait()
        for _ in range(20):
            item = p.consume()
            if item is not None:
                results.append(item)
    pt = threading.Thread(target=producer, daemon=True)
    ct = threading.Thread(target=consumer, daemon=True)
    pt.start()
    ct.start()
    barrier.wait()
    pt.join()
    ct.join()
    assert len(results) == 20
    assert sorted(results) == list(range(20))
