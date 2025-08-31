import os
import socket
import sys
from pathlib import Path
import signal
import sys
import threading

parent_dir = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(parent_dir))

from internal.server.server import serve


if __name__ == "__main__":
    port = 42069
    
    s = serve(port)

    def handle_signal(signum, frame):
        print(f"signum={signum} frame={frame}, Server gracefully stopped")
        s.close()

    # Register signal handlers
    signal.signal(signal.SIGINT, handle_signal)   # Handle Ctrl+C (SIGINT)
    signal.signal(signal.SIGTERM, handle_signal)  # Handle termination signal (SIGTERM)

    # Wait indefinitely until a signal is received
    signal.pause()

