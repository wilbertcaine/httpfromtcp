import io
from request import request_from_reader

class ChunkReader:
    def __init__(self, data, num_bytes_per_read):
        self.data = data
        self.num_bytes_per_read = num_bytes_per_read
        self.pos = 0

    def read(self, size):
        if self.pos >= len(self.data):
            return b"", io.EOF
        end_index = self.pos + self.num_bytes_per_read
        if end_index > len(self.data):
            end_index = len(self.data)
        chunk = self.data[self.pos:end_index].encode()
        n = len(chunk)
        self.pos += n
        return chunk[:size], None



def test_good_get_request():
    reader = io.StringIO("GET / HTTP/1.1\r\nHost: localhost:42069\r\nUser-Agent: curl/7.81.0\r\nAccept: */*\r\n\r\n")
    r, err = request_from_reader(reader)
    assert err is None, f"Expected no error, got {err}"
    assert r is not None, "Expected Request object"
    assert r.request_line.method == "GET"
    assert r.request_line.request_target == "/"
    assert r.request_line.http_version == "1.1"

def test_good_get_request_with_path():
    reader = io.StringIO("GET /coffee HTTP/1.1\r\nHost: localhost:42069\r\nUser-Agent: curl/7.81.0\r\nAccept: */*\r\n\r\n")
    r, err = request_from_reader(reader)
    assert err is None, f"Expected no error, got {err}"
    assert r is not None, "Expected Request object"
    assert r.request_line.method == "GET"
    assert r.request_line.request_target == "/coffee"
    assert r.request_line.http_version == "1.1"

def test_invalid_request_line():
    reader = io.StringIO("/coffee HTTP/1.1\r\nHost: localhost:42069\r\nUser-Agent: curl/7.81.0\r\nAccept: */*\r\n\r\n")
    r, err = request_from_reader(reader)
    assert err is not None, "Expected an error"
    assert r is None, "Expected no Request object"

if __name__ == "__main__":
    test_good_get_request()
    test_good_get_request_with_path()
    test_invalid_request_line()
    print("All tests passed!")


