from dataclasses import dataclass
import io
import re

@dataclass
class RequestLine:
    http_version: str = ""
    request_target: str = ""
    method: str = ""

@dataclass
class Request:
    request_line: RequestLine

CLRF = r'\r\n'


def request_from_reader(reader: io.TextIOBase) -> tuple[Request | None, Exception | None]:
    data = reader.read()
    data = re.split(CLRF, str(data))

    request_line = data.pop(0)
    request_line = request_line.split()

    method = http_version = ''
    if (method := request_line.pop(0)) and not method.isupper():
        return None, Exception(f'method={method} is not upper')
    if not (request_target := request_line.pop(0)):
        return None, Exception(f'request_target={request_target} not found')
    if (http_version := request_line.pop(0)) and http_version != 'HTTP/1.1':
        return None, Exception(f'http_version={http_version} is not HTTP/1.1')
    return Request(RequestLine('1.1', request_target, method)), None

