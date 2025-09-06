import os
import socket
import sys
from pathlib import Path
import signal
import sys
import threading

import requests
from time import sleep


parent_dir = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(parent_dir))

from internal.server import server
from internal.request import request
from internal.response import response


BAD = '''<html>
  <head>
    <title>400 Bad Request</title>
  </head>
  <body>
    <h1>Bad Request</h1>
    <p>Your request honestly kinda sucked.</p>
  </body>
</html>'''

ERROR = '''<html>
  <head>
    <title>500 Internal Server Error</title>
  </head>
  <body>
    <h1>Internal Server Error</h1>
    <p>Okay, you know what? This one is on me.</p>
  </body>
</html>'''

OK = '''<html>
  <head>
    <title>200 OK</title>
  </head>
  <body>
    <h1>Success!</h1>
    <p>Your request was an absolute banger.</p>
  </body>
</html>'''

def get_headers(msg: str, curr_headers: dict):
    headers = response.get_default_header(len(msg))
    if 'Transfer-Encoding' in curr_headers:
        headers.headers.pop('Content-Length')
    headers.headers.update(curr_headers)
    return headers

def handle_str(conn:socket.socket, handler_error: server.HandlerError):
    writer = response.Writer(conn)
    writer.write_status_line(handler_error.status_code)
    writer.write_headers(get_headers(handler_error.msg, handler_error.headers))
    writer.write_body(handler_error.msg)

def handle_httpbin(conn: socket.socket, headers: dict, target: str):
    writer = response.Writer(conn)
    writer.write_status_line(response.StatusCode.OK)
    writer.write_headers(get_headers('', headers))
    
    #print(target)
    httpbin_response = requests.get(target, stream=True)
    for chunk in httpbin_response.iter_content(64):
        if chunk:
            print(chunk)
            writer.write_chunked_body(chunk.decode())
            sleep(1)
    writer.write_chunked_body_done()


def handler(conn:socket.socket, request: request.Request) -> server.HandlerError:
    headers = {'Content-Type': 'text/html'}
    if request.request_line.request_target.startswith('/httpbin'):
        target = 'https://httpbin.org' + request.request_line.request_target.removeprefix('/httpbin')
        status_code, msg = response.StatusCode.InternalServerError, f'{ERROR}\n'
        headers['Transfer-Encoding'] = 'chunked'
        handler_error = server.HandlerError(response.StatusCode.OK, '', headers)
        print(target)
        handle_httpbin(conn, headers, target)
    else:
        status_code, msg = response.StatusCode.OK, f'{OK}\n'
        if request.request_line.request_target == '/yourproblem':
            status_code, msg = response.StatusCode.BadRequest, f'{BAD}\n'
        elif request.request_line.request_target == '/myproblem':
            status_code, msg = response.StatusCode.InternalServerError, f'{ERROR}\n'
        handler_error = server.HandlerError(status_code, msg, headers)
        handle_str(conn, handler_error)

    conn.close()
    return handler_error


if __name__ == "__main__":
    port = 42069
    
    #s = server.serve(port, handler_str)
    s = server.serve(port, handler)

    def handle_signal(signum, frame):
        print(f"signum={signum} frame={frame}, Server gracefully stopped")
        s.close()

    # Register signal handlers
    signal.signal(signal.SIGINT, handle_signal)   # Handle Ctrl+C (SIGINT)
    signal.signal(signal.SIGTERM, handle_signal)  # Handle termination signal (SIGTERM)

    # Wait indefinitely until a signal is received
    signal.pause()

