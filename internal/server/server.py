import sys
import socket
from pathlib import Path

parent_dir = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(parent_dir))

from internal.request.request import request_from_reader

class Server:
    def __init__(self, s):
        self.s = s

    def close(self):
        self.s.close()

    def listen(self):
        self.s.listen()
        conn, addr = self.s.accept()
        conn.setblocking(False)

        print(f'addr={addr}')
        self.handle(conn)

    def handle(self, conn):
        fd = conn.makefile('rb')
        request, err = request_from_reader(fd)
        print('done request_from_header')
        if err:
            print(err)
        print('Request Line:')
        print(f'- Method: {request.request_line.method}')
        print(f'- Target: {request.request_line.request_target}')
        print(f'- Version: {request.request_line.http_version}')
        print('Headers')
        for k, v in request.headers.headers.items():
            print(f'- {k}: {v}')
        print('Body:')
        print(request.body)

        data = b'''HTTP/1.1 200 OK
        Content-Type: text/plain
        Content-Length: 13
        
        Hello World!'''
        conn.sendall(data)
        self.s.close()


def serve(port: int):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(('localhost', 42069))

    s = Server(s)
    s.listen()
    return s

