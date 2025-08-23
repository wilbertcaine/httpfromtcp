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

def read_from_file():
    fd = os.open('/Users/wilbertcaine/Projects/httpfromtcp/messages.txt', os.O_RDONLY)
    for line in get_lines_channel(fd):
        print(line)

def get_lines_address(address):
    s = socket.socket()
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
    #read_from_file()

    for line in get_lines_address(('localhost', 42069)):
        print(line)

