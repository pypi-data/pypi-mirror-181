import json


class Downlink:
    def __init__(self):
        self.body = ""
        self.status = "200 "
        self.headers = []

    def __iter__(self):
        for b in self.body:
            if isinstance(b, bytes):
                yield b
            else:
                yield b.encode()

    def code(self, code):
        self.status = f"{code} "
        return self

    def header(self, name, value):
        self.headers = [h for h in self.headers if name != h[0]]
        self.headers.append((name, value))

        return self

    def content(self, type):
        self.header("Content-type", type)

    def json(self, data):
        self.content("application/json")
        self.body = json.dumps(data)

        return self

    def text(self, data):
        self.content("text/plain")
        self.body = str(data)

        return self
