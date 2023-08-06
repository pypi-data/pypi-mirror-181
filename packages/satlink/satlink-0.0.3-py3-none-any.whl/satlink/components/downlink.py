from datetime import timedelta, datetime
import json
from time import mktime
from wsgiref.handlers import format_date_time


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
        self.header("Content-Type", type)

    def json(self, data):
        self.content("application/json")
        self.body = json.dumps(data)

        return self

    def text(self, data):
        self.content("text/plain")
        self.body = str(data)

        return self

    def redirect(self, url):
        self.header("Location", url)
        self.code(301)

        return self

    def cookie(self, name, value, expires=datetime.now() + timedelta(days=42)):
        expires = mktime(expires.timetuple())
        expires = format_date_time(expires)
        self.header("Set-Cookie", f"{name}={value}; Expires={expires}")

        return self

    def eat(self, name):
        return self.cookie(name, '', datetime(1970, 1, 1))
