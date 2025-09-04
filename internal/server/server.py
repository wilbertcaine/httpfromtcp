import sys
import socket
from pathlib import Path
import asyncio
from collections.abc import Callable

parent_dir = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(parent_dir))

from internal.request import request
from internal.response import response

#semaphore = asyncio.Semaphore()

class HandlerError:
    def __init__(self, status_code: response.StatusCode, msg: str) -> None:
        self.status_code = status_code
        self.msg = msg

class Server:
    def __init__(self, s, handler: Callable[[request.Request], HandlerError]):
        self.s = s
        self.handler = handler

    def close(self):
        print('closing')
        self.s.close()

    def listen(self):
        while True:
            self.s.listen()
            conn, addr = self.s.accept()
            conn.setblocking(False)

            print(f'addr={addr}')
            self.handle(conn)

    def handle(self, conn):
        fd = conn.makefile('rb')
        req, err = request.request_from_reader(fd)
        print('done request_from_header')
        if err:
            print(err)
        print('Request Line:')
        print(f'- Method: {req.request_line.method}')
        print(f'- Target: {req.request_line.request_target}')
        print(f'- Version: {req.request_line.http_version}')
        print('Headers')
        for k, v in req.headers.headers.items():
            print(f'- {k}: {v}')
        print('Body:')
        print(req.body)

        handler_error = self.handler(req)

        #data = b'HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\nContent-Length: 13\r\n\r\nHello World!\n'
        #conn.sendall(data)
        headers = response.get_default_header(len(handler_error.msg))

        writer = response.Writer(conn)
        writer.write_status_line(handler_error.status_code)
        writer.write_headers(headers)
        writer.write_body(handler_error.msg)

        conn.close()


def serve(port: int, handler: Callable[[request.Request], HandlerError]):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(('localhost', port))

    print(f'Server started on port={port}')

    s = Server(s, handler)
    s.listen()
    return s

