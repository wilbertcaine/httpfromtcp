import os
import socket
import sys
from pathlib import Path

parent_dir = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(parent_dir))

from internal.request.request import request_from_reader


if __name__ == "__main__":
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(('localhost', 42069))
    s.listen()
    conn, addr = s.accept()
    fd = conn.makefile('rb')
    print(f'addr={addr}')
    request, err = request_from_reader(fd)
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
    s.close()

