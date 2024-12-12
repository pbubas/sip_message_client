class SipServerResponse:
    def __init__(self, code, header, body):
        self.code = code
        self.header = header
        self.body = body
        self.ok = True if "202 Accepted" in code else False

    @property
    def encoded(self):
        header=dict()
        header = {k:v for k,v in self.header.items()}
        try:
            header['WWW-Authenticate'] = ''.join(f'{k}={v}, ' for k,v in header['WWW-Authenticate'].items()).rstrip(', ')
        except KeyError:
            pass
        message = f'{self.code}\r\n' + ''.join(f'{k}: {v}\r\n' for k,v in header.items())
        message = message + '\r\n' + self.body
        return message.encode()

    @classmethod
    def decode(cls, binary: bytes):
        code, header = binary.decode().split("\r\n", 1)
        header = header.split("\r\n")
        body=header[-1]
        header_lines = map(cls._header_line_to_dict, header)
        header = dict()
        header = {items[0]:items[1] for items in header_lines if items}
        if 'WWW-Authenticate' in header:
            scheme, www_authenticate = header['WWW-Authenticate'].split(' ', 1)
            header['WWW-Authenticate'] = cls._parameters_to_dict(www_authenticate, ",")
            header['WWW-Authenticate']['scheme'] = scheme
        try: 
            header['Via'] = cls._parameters_to_dict(header['Via'], ";")
        except KeyError:
            pass
        return cls(code, header, body)

    @staticmethod
    def _header_line_to_dict(header_line: str):
        try:
            key, value = header_line.split(":", 1)
        except ValueError:
            return None
        return key, value.strip()

    @staticmethod
    def _parameters_to_dict(parameters: str, seperator: str):
        parameters = parameters.split(f'{seperator}')
        parameters = filter(lambda x: "=" in x, parameters)
        parameters = map(lambda x: x.split("="), parameters)
        return {k.strip():v.strip() for k,v in parameters}
    