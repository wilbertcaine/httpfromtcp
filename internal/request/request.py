from dataclasses import dataclass
import io
import re
#from request_test import ChunkReader
from enum import Enum, auto

import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))

from headers.headers import Headers



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
        n = idx + 2
        return n, None

class RequestState(Enum):
    INIT = auto()
    HEAD = auto()
    BODY = auto()
    DONE = auto()

@dataclass
class Request:
    request_line: RequestLine
    headers: Headers
    body: str
    request_state: RequestState

    def parse_single(self, data: bytes) -> tuple[int, Exception | None]:
        n, err = 0, None
        match self.request_state:
            case RequestState.INIT:
                n, err = self.request_line.parse_request_line(data)
                if n and err is None:
                    self.request_state = RequestState.HEAD
            case RequestState.HEAD:
                n, done, err = self.headers.parse(data)
                if done:
                    self.request_state = RequestState.DONE
            case RequestState.DONE:
                pass
        return n, err

    def parse(self, data: bytes) -> tuple[int, Exception | None]:
        n, err = 0, None
        while self.request_state != RequestState.DONE:
            read, err = self.parse_single(data[n:])
            #print(data[n:], self.request_line, self.headers.headers)
            n += read
            if read == 0 or err:
                break
        return n, err


def request_from_reader(reader) -> tuple[Request, Exception | None]:
    request, err = Request(RequestLine(), Headers(), RequestState.INIT), None
    data = b''
    while request.request_state != RequestState.DONE:
        new_data = reader.read()
        data += new_data
        n, err = request.parse(data)
        if err:
            print(err)
            break
        data = data[n:]
    return request, err

