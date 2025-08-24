import unittest
from headers import Headers

class TestHeaders(unittest.TestCase):
    def test_valid_done(self):
        headers = Headers()
        data = b"\r\n\r\n"
        n, done, err = headers.parse(data)
        self.assertIsNone(err)
        #self.assertIsNotNone(headers.headers)
        #self.assertEqual(headers.headers.get("Host"), "localhost:42069")
        self.assertEqual(n, 0)
        self.assertTrue(done)

    def test_2_valid_with_existing_header(self):
        headers = Headers()
        data = b"Host: localhost:42069\r\n\r\n"
        n, done, err = headers.parse(data)
        self.assertIsNone(err)
        self.assertIsNotNone(headers.headers)
        self.assertEqual(headers.headers.get("Host"), "localhost:42069")
        self.assertEqual(n, 23)
        self.assertFalse(done)

        data = b"Host: localhost:again\r\n\r\n"
        n, done, err = headers.parse(data)
        self.assertIsNone(err)
        self.assertIsNotNone(headers.headers)
        self.assertEqual(headers.headers.get("Host"), "localhost:42069, localhost:again")
        self.assertEqual(n, 23)
        self.assertFalse(done)

    def test_valid_single_header(self):
        headers = Headers()
        data = b"Host: localhost:42069\r\n\r\n"
        n, done, err = headers.parse(data)
        self.assertIsNone(err)
        self.assertIsNotNone(headers.headers)
        self.assertEqual(headers.headers.get("Host"), "localhost:42069")
        self.assertEqual(n, 23)
        self.assertFalse(done)

    def test_invalid_spacing_header(self):
        headers = Headers()
        data = b"       Host : localhost:42069       \r\n\r\n"
        n, done, err = headers.parse(data)
        self.assertIsNotNone(err)
        self.assertEqual(n, 0)
        self.assertFalse(done)

    def test_invalid_character_header(self):
        headers = Headers()
        data = b"H@st: localhost:42069\r\n\r\n"
        n, done, err = headers.parse(data)
        self.assertIsNotNone(err)
        self.assertEqual(n, 0)
        self.assertFalse(done)

if __name__ == "__main__":
    unittest.main(verbosity=2)
