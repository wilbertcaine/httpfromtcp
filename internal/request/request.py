from dataclasses import dataclass
import io
import re
#from request_test import ChunkReader
from enum import Enum


CLRF = b'\r\n' 

@dataclass
class RequestLine:
    http_version: str = ""
    request_target: str = ""
    method: str = ""

    def parse_request_line(self, data: bytes) -> tuple[int, Exception | None]:
        idx = data.find(CLRF)
        if idx == -1:
            return 0, None
    
        request_line_data = data[:idx].split()
        if len(request_line_data) != 3:
            return 0, Exception(f'request_line_data={request_line_data} invalid')
        method, request_target, http_version = request_line_data
        if not method.isupper():
            return 0, Exception(f'method={method} is not upper')
        if http_version != b'HTTP/1.1':
            return 0, Exception(f'http_version={http_version} is not HTTP/1.1')
        http_version = '1.1'
        self.__init__(http_version, request_target.decode(), method.decode())
        return idx, None

class RequestState(Enum):
    INIT = 1
    DONE = 2

@dataclass
class Request:
    request_line: RequestLine
    request_state: RequestState

    def parse(self, data: bytes) -> tuple[int, Exception | None]:
        match self.request_state:
            case RequestState.INIT:
                n, err = self.request_line.parse_request_line(data)
                if n and err is None:
                    self.request_state = RequestState.DONE
                return n, err
            case RequestState.DONE:
                return 0, None


def request_from_reader(reader) -> tuple[Request, Exception | None]:
    request = Request(RequestLine(), RequestState.INIT)
    data = b''
    while request.request_state != RequestState.DONE:
        new_data = reader.read()
        data += new_data
        n, err = request.parse(data)
        if err:
            print(err)
        data = data[n:]
    return request, None

