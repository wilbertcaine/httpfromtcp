import os
import socket
import sys
from pathlib import Path
import signal
import sys
import threading

parent_dir = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(parent_dir))

from internal.server import server
from internal.request import request
from internal.response import response


def handler_str(request: request.Request) -> server.HandlerError:
    status_code, msg = response.StatusCode.OK, 'All good, frfr\n'
    if request.request_line.request_target == '/yourproblem':
        status_code, msg = response.StatusCode.BadRequest, 'Your problem is not my problem\n'
    elif request.request_line.request_target == '/myproblem':
        status_code, msg = response.StatusCode.InternalServerError, 'Woopsie, my bad\n"'
    return server.HandlerError(status_code, msg)


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


def handler(request: request.Request) -> server.HandlerError:
    status_code, msg = response.StatusCode.OK, f'{OK}\n'
    if request.request_line.request_target == '/yourproblem':
        status_code, msg = response.StatusCode.BadRequest, f'{BAD}\n'
    elif request.request_line.request_target == '/myproblem':
        status_code, msg = response.StatusCode.InternalServerError, f'{ERROR}\n"'
    return server.HandlerError(status_code, msg)


if __name__ == "__main__":
    port = 42069
    
    s = server.serve(port, handler)

    def handle_signal(signum, frame):
        print(f"signum={signum} frame={frame}, Server gracefully stopped")
        s.close()

    # Register signal handlers
    signal.signal(signal.SIGINT, handle_signal)   # Handle Ctrl+C (SIGINT)
    signal.signal(signal.SIGTERM, handle_signal)  # Handle termination signal (SIGTERM)

    # Wait indefinitely until a signal is received
    signal.pause()

