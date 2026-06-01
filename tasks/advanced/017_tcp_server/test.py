import socket
import threading
import time
from buggy import start_server

def test_echo():
    HOST, PORT = "127.0.0.1", 19876
    t = threading.Thread(target=start_server, args=(HOST, PORT), daemon=True)
    t.start()
    time.sleep(0.1)
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((HOST, PORT))
    client.sendall(b"hello")
    data = client.recv(1024)
    assert data == b"hello"
    client.sendall(b"world")
    data = client.recv(1024)
    assert data == b"world"
    client.close()
