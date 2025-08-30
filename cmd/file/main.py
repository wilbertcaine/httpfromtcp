import os

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
    fd = os.open('/Users/wilbertcaine/Projects/httpfromtcp/messages.txt', os.O_RDONLY)
    for line in get_lines_channel(fd):
        print(line)

