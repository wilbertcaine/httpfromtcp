import os
import socket

if __name__ == "__main__":
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    addr = ('localhost', 42069)
    print(f'addr={addr}')

    while True:
        data = input('>')
        s.sendto(data.encode(), addr)
    s.close()

