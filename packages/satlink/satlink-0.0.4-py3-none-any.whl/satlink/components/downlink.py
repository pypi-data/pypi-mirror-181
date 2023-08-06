from datetime import timedelta, datetime
import json
from time import mktime
from typing import Dict, List, Tuple
from wsgiref.handlers import format_date_time


class Downlink:
    def __init__(self):
        self.body = ""
        self.status = "200 "
        self.headers: List[Tuple] = []

    def __iter__(self):
        for b in self.body:
            if isinstance(b, bytes):
                yield b
            else:
                yield b.encode()

    def code(self, code: int):
        self.status = f"{code} "
        return self

    def header(self, name: str, value: str):
        self.headers = [h for h in self.headers if name != h[0]]
        self.headers.append((name, value))

        return self

    def content(self, type: str):
        self.header("Content-Type", type)

    def json(self, data: Dict | List[Dict]):
        self.content("application/json")
        self.body = json.dumps(data)

        return self

    def text(self, data: str):
        self.content("text/plain")
        self.body = str(data)

        return self

    def redirect(self, url: str):
        self.header("Location", url)
        self.code(301)

        return self

    def cookie(self, name: str, value: str, expires=datetime.now() + timedelta(days=42)):
        expires = mktime(expires.timetuple())
        expires = format_date_time(expires)
        self.header("Set-Cookie", f"{name}={value}; Expires={expires}")

        return self

    def eat(self, name: str):
        return self.cookie(name, '', datetime(1970, 1, 1))
