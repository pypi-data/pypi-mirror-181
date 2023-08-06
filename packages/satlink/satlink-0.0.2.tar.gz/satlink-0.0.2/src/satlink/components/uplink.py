from enum import Enum
import json


class Uplink:
    def __init__(self, environ, query):
        self.__environ = environ
        self.__query = query

    @property
    def body(self):
        c_length = int(self.__environ['CONTENT_LENGTH'])
        c_type = self.__environ['CONTENT_TYPE']
        content = self.__environ['wsgi.input'].read(c_length).decode()

        if "application/json" in c_type:
            return json.loads(content)
        else:
            return content

    @property
    def query(self):
        return self.__query


class Method(Enum):
    GET = "GET",
    POST = "POST",
    PUT = "PUT",
    PATCH = "PATCH",
    DELETE = "DELETE"
