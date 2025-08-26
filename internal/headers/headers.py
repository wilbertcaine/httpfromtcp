from typing import Dict, Tuple

CLRF = b'\r\n'

class CaseInsensitiveDict(dict):
    def __getitem__(self, key):
        return super().__getitem__(key.casefold())
    
    def __setitem__(self, key, value):
        super().__setitem__(key.casefold(), value)
    
    def __delitem__(self, key):
        super().__delitem__(key.casefold())
    
    def __contains__(self, key):
        return super().__contains__(key.casefold())

    def get(self, key, default=None):
        return super().get(key.casefold(), default)


class Headers:
    def __init__(self):
        self.headers: Dict[str, str] = CaseInsensitiveDict()

    def get(self, key, default=None):
        return self.headers.get(key, default)

    def parse(self, data: bytes) -> Tuple[int, bool, Exception | None]:
        n = 0
        idx = data[n:].find(CLRF)
        if idx == -1:
            return (0, False, None)
        if idx == 0:
            n += 2
            return (n, True, None)
        header = data[n:n+idx].lstrip(b' ').rstrip(b' ')
        header = header.decode().split()
        if len(header) != 2:
            return (0, False, Exception(f'header={header} invalid'))
        field_name, field_value = header
        if field_name[-1] != ':':
            return (0, False, Exception(f'header={header} invalid'))
        field_name = field_name[:-1]
        if not all(c.isalnum() or c in "!, #, $, %, &, ', *, +, -, ., ^, _, `, |, ~".split(', ') for c in field_name):
            return (0, False, Exception(f'field_name={field_name} invalid'))
        field_name = field_name.lower()
        if field_name in self.headers:
            self.headers[field_name] += ', ' + field_value
        else:
            self.headers[field_name] = field_value
        n = idx + 2
        return (n, False, None)
