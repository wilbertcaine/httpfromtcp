import io

import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))

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
        end_index = min(self.pos + self.num_bytes_per_read, len(self.data))
        chunk = self.data[self.pos:end_index].encode()
        self.pos = end_index
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

    def test_standard_headers(self):
        reader = ChunkReader(
            data="GET / HTTP/1.1\r\nHost: localhost:42069\r\nUser-Agent: curl/7.81.0\r\nAccept: */*\r\n\r\n",
            num_bytes_per_read=3
        )
        r, err = request_from_reader(reader)
        #print(f'headers={r.headers.headers}')
        self.assertIsNone(err)
        self.assertIsNotNone(r)
        self.assertEqual(r.headers.get("host"), "localhost:42069")
        self.assertEqual(r.headers.get("user-agent"), "curl/7.81.0")
        self.assertEqual(r.headers.get("accept"), "*/*")

    def test_malformed_header(self):
        reader = ChunkReader(
            data="GET / HTTP/1.1\r\nHost localhost:42069\r\n\r\n",
            num_bytes_per_read=3
        )
        r, err = request_from_reader(reader)
        self.assertIsNotNone(err)

    def test_standard_body(self):
        reader = ChunkReader(
            data="POST /submit HTTP/1.1\r\nHost: localhost:42069\r\nContent-Length: 13\r\n\r\nhello world!\n",
            num_bytes_per_read=3
        )
        r, err = request_from_reader(reader)
        self.assertIsNone(err)
        self.assertIsNotNone(r)
        self.assertEqual(r.body, "hello world!\n")

    def empty_body_zero_content_length(self):
        reader = ChunkReader(
            data="POST /submit HTTP/1.1\r\nHost: localhost:42069\r\nContent-Length: 0\r\n\r\n",
            num_bytes_per_read=3
        )
        r, err = request_from_reader(reader)
        self.assertIsNone(r.body)
        self.assertIsNone(err)

    def empty_body_no_content_length(self):
        reader = ChunkReader(
            data="POST /submit HTTP/1.1\r\nHost: localhost:42069\r\n\r\n",
            num_bytes_per_read=3
        )
        r, err = request_from_reader(reader)
        self.assertIsNone(r.body)
        self.assertIsNone(err)

    def test_body_shorter_than_content_length(self):
        reader = ChunkReader(
            data="POST /submit HTTP/1.1\r\nHost: localhost:42069\r\nContent-Length: 20\r\n\r\npartial content",
            num_bytes_per_read=3
        )
        r, err = request_from_reader(reader)
        self.assertIsNotNone(err)

    def test_standard_body_no_content_length(self):
        reader = ChunkReader(
            data="POST /submit HTTP/1.1\r\nHost: localhost:42069\r\n\r\nhello world!\n",
            num_bytes_per_read=3
        )
        r, err = request_from_reader(reader)
        self.assertIsNone(err)
        self.assertIsNotNone(r)
        #self.assertEqual(r.body, "hello world!\n")

if __name__ == '__main__':
    unittest.main()
