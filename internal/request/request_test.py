import io
from request import request_from_reader
import unittest

class ChunkReader:
    def __init__(self, data, num_bytes_per_read):
        self.data = data
        self.num_bytes_per_read = num_bytes_per_read
        self.pos = 0

    def read(self):
        if self.pos >= len(self.data):
            return b""
        end_index = self.pos + self.num_bytes_per_read
        if end_index > len(self.data):
            end_index = len(self.data)
        chunk = self.data[self.pos:end_index].encode()
        n = len(chunk)
        self.pos += n
        return chunk

class TestChunkReader(unittest.TestCase):
    def test_good_get_request_line(self):
        reader = ChunkReader(
            data="GET / HTTP/1.1\r\nHost: localhost:42069\r\nUser-Agent: curl/7.81.0\r\nAccept: */*\r\n\r\n",
            num_bytes_per_read=3
        )
        r, err = request_from_reader(reader)
        self.assertIsNone(err, "Expected no error")
        self.assertIsNotNone(r, "Expected request object to be not None")
        self.assertEqual(r.request_line.method, "GET", "method should be GET")
        self.assertEqual(r.request_line.request_target, "/", "request_target should be /")
        self.assertEqual(r.request_line.http_version, "1.1", "http_version should be 1.1")

    def test_good_get_request_line_with_path(self):
        reader = ChunkReader(
            data="GET /coffee HTTP/1.1\r\nHost: localhost:42069\r\nUser-Agent: curl/7.81.0\r\nAccept: */*\r\n\r\n",
            num_bytes_per_read=1
        )
        r, err = request_from_reader(reader)
        self.assertIsNone(err, "Expected no error")
        self.assertIsNotNone(r, "Expected request object to be not None")
        self.assertEqual(r.request_line.method, "GET", "method should be GET")
        self.assertEqual(r.request_line.request_target, "/coffee", "request_target should be /coffee")
        self.assertEqual(r.request_line.http_version, "1.1", "http_version should be 1.1")

if __name__ == '__main__':
    unittest.main()
