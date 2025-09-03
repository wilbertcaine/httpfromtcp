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

def write_status_line(conn, status_code):
    match status_code:
        case StatusCode.OK:
            conn.send(b'HTTP/1.1 200 OK\r\n')
        case StatusCode.BadRequest:
            conn.send(b'HTTP/1.1 400 Bad Request\r\n')
        case StatusCode.InternalServerError:
            conn.send(b'HTTP/1.1 500 Internal Server Error\r\n')
        case _:
            return Exception(f'status_code={status_code} not found')
    return None

def get_default_header(content_length) -> Headers:
    headers = Headers()
    headers.headers.__setitem__('Content-Length', content_length)
    headers.headers.__setitem__('Connection', 'close')
    headers.headers.__setitem__('Content-Type', 'text/plain')
    return headers

def send(conn, data):
    data = data.encode()
    n = conn.send(data)
    if n != len(data):
        return Exception(f'send={n}, data={data} len={len(data)}')

def write_headers(conn: socket.socket, headers: Headers):
    for k, v in headers.headers.items():
        if err := send(conn, f'{k}: {v}\r\n'):
            return err
    if err := send(conn, '\r\n'):
        return err

def write_body(conn: socket.socket, body: str):
    if err := send(conn, body):
        return err
