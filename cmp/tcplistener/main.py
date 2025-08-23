import os
import socket

def get_lines_address(address):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(address)
    s.listen()
    conn, addr = s.accept()
    print(f'addr={addr}')

    curr = ''
    while data := conn.recv(8):
        data = data.decode()
        data = data.split('\n')
        while len(data) > 1:
            curr += data.pop(0)
            yield curr
            curr = ''
        curr += data.pop(0)
    s.close()


if __name__ == "__main__":
    for line in get_lines_address(('localhost', 42069)):
        print(line)

