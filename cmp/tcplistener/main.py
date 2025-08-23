import os
import socket

def get_lines_channel(fd):
    curr = ''
    while data := os.read(fd, 8):
        data = data.decode()
        data = data.split('\n')
        while len(data) > 1:
            curr += data.pop(0)
            yield curr
            curr = ''
        curr += data.pop(0)
    os.close(fd)


if __name__ == "__main__":
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(('localhost', 42069))
    s.listen()
    conn, addr = s.accept()
    print(f'addr={addr}')
    for line in get_lines_channel(conn.fileno()):
        print(line)

