import os
import socket
import sys
from pathlib import Path

parent_dir = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(parent_dir))

from internal.server.server import serve


if __name__ == "__main__":
    port = 42069
    server = serve(port)

    print(f'Server started on port={port}')
    print('Server gracecully stopped')

