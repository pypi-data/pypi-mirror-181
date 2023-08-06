from wsgiref.simple_server import make_server
from .server import server
from .uplink import Method


class Satellite:
    """
    🛰 SATLINK

    A light web framework - originally developed as a project 
    in Frameworks at HiØ, written with love in Python <3

    Authors:
        (@olejorga): Ole-Jørgen Andersen
    """

    def __init__(self):
        self.endpoints = []

    def get(self, route):
        return self.__endpoint(Method.GET, route)

    def post(self, route):
        return self.__endpoint(Method.POST, route)

    def put(self, route):
        return self.__endpoint(Method.PUT, route)

    def patch(self, route):
        return self.__endpoint(Method.PATCH, route)

    def delete(self, route):
        return self.__endpoint(Method.DELETE, route)

    def __endpoint(self, method, route):
        def inner(controller):
            self.endpoints.append((method, route, controller))

        return inner

    def transmit(self, port=3000, host="localhost"):
        print(Satellite.__doc__)
        print('\u001b[38;5;246m')

        try:
            with make_server(host, port, server(self.endpoints)) as app:
                app.serve_forever()
                print(f"Satellite listening on http://{host}:{port}")
        except KeyboardInterrupt:
            app.server_close()
