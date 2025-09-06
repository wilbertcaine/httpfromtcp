from enum import Enum, auto
from pathlib import Path
import sys
import socket

parent_dir = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(parent_dir))

from internal.headers.headers import Headers

class StatusCode(Enum):
    OK = 200
    BadRequest = 400
    InternalServerError = 500

def get_default_header(content_length) -> Headers:
    headers = Headers()
    headers.headers.__setitem__('Content-Length', content_length)
    headers.headers.__setitem__('Connection', 'close')
    headers.headers.__setitem__('Content-Type', 'text/plain')
    #headers.headers.__setitem__('Content-Type', 'text/html')
    return headers

class Writer:
    def __init__(self, conn: socket.socket):
        self.conn = conn

    def write_status_line(self, status_code):
        match status_code:
            case StatusCode.OK:
                self.send('HTTP/1.1 200 OK\r\n')
            case StatusCode.BadRequest:
                self.send('HTTP/1.1 400 Bad Request\r\n')
            case StatusCode.InternalServerError:
                self.send('HTTP/1.1 500 Internal Server Error\r\n')
            case _:
                return Exception(f'status_code={status_code} not found')
        return None

    def send(self, data):
        data = data.encode()
        print(data)
        n = self.conn.send(data)
        if n != len(data):
            return Exception(f'send={n}, data={data} len={len(data)}')

    def write_headers(self, headers: Headers):
        for k, v in headers.headers.items():
            if err := self.send(f'{k}: {v}\r\n'):
                return err
        if err := self.send('\r\n'):
            return err

    write_trailers = write_headers

    def write_body(self, body: str):
        if err := self.send(body):
            return err

    def write_chunked_body(self, body: str):
        n = 0
        while n < len(body):
            end = min(n + 32, len(body))
            if err := self.send(f'{end - n:x}\r\n'):
                return err
            if err := self.send(f'{body[n: end]}\r\n'):
                return err
            n = end

    def write_chunked_body_done(self):
        if err := self.send('0\r\n'):
            return err
        if err := self.send('\r\n'):
            return err

