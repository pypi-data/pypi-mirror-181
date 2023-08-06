from typing import List
from wsgiref.simple_server import make_server
from .type import Endpoint, Handler
from .server import server
from .uplink import Method


LOGO = """
⠀⠀⠀⣤⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣤⠀⠀⠀⠀⠀⠀⠀⠀⣠⣦⡀⠀⠀⠀
⠀⠀⠛⣿⠛⠀⠀⠀⠀⠀⠀⠀⠀⠀⠛⣿⠛⠀⠀⠀⠀⠀⡀⠺⣿⣿⠟⢀⡀⠀
⠀⠀⠀⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣠⣾⣿⣦⠈⠁⣴⣿⣿⡦
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣠⣦⡈⠻⠟⢁⣴⣦⡈⠻⠋⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣤⡀⠺⣿⣿⠟⢀⡀⠻⣿⡿⠋⠀⠀⠀
⠀⣠⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢠⣶⡿⠿⣿⣦⡈⠁⣴⣿⣿⡦⠈⠀⠀⠀⠀⠀
⠲⣿⠷⠂⠀⠀⠀⠀⠀⠀⢀⣴⡿⠋⣠⣦⡈⠻⣿⣦⡈⠻⠋⠀⠀⠀⠀⠀⠀⠀
⠀⠈⠀⠀⠀⠀⠀⠀⠀⠰⣿⣿⡀⠺⣿⣿⣿⡦⠈⣻⣿⡦⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⣠⣦⡈⠻⣿⣦⡈⠻⠋⣠⣾⡿⠋⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⡀⠺⣿⣿⠟⢀⡈⠻⣿⣶⣾⡿⠋⣠⣦⡀⠀⢀⣠⣤⣀⡀⠀⠀
⠀⠀⠀⠀⣠⣾⣿⣦⠈⠁⣴⣿⣿⡦⠈⠛⠋⠀⠀⠈⠛⢁⣴⣿⣿⡿⠋⠀⠀⠀
⠀⠀⣠⣦⡈⠻⠟⢁⣴⣦⡈⠻⠋⠀⠀⠀⠀⠀⠀⠀⣴⣿⣿⣿⣏⠀⠀⠀⠀⠀
⠀⠺⣿⣿⠟⢀⡀⠻⣿⡿⠋⠀⠀⠀⠀⠀⠀⠀⠀⠰⣿⡿⠛⠁⠙⣷⣶⣦⠀⠀
⠀⠀⠈⠁⣴⣿⣿⡦⠈⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠋⠀⠀⠀⠀⠻⠿⠟⠀⠀
⠀⠀⠀⠀⠈⠻⠋⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
"""


class Satellite:
    """
    SATLINK

    A light web framework - originally developed as a project 
    in Frameworks at HiØ, written with love in Python <3

    Authors:
        (@olejorga): Ole-Jørgen Andersen
    """

    def __init__(self):
        self.endpoints: List[Endpoint] = []

    def get(self, route: str):
        return self.__endpoint(Method.GET, route)

    def post(self, route: str):
        return self.__endpoint(Method.POST, route)

    def put(self, route: str):
        return self.__endpoint(Method.PUT, route)

    def patch(self, route: str):
        return self.__endpoint(Method.PATCH, route)

    def delete(self, route: str):
        return self.__endpoint(Method.DELETE, route)

    def __endpoint(self, method: Method, route: str):
        def inner(handler: Handler):
            self.endpoints.append((method, route, handler))

        return inner

    def transmit(self, port=3000, host="localhost"):
        print(LOGO)
        print(Satellite.__doc__)
        print('\u001b[38;5;246m')  # Mute terminal text color.

        try:
            with make_server(host, port, server(self.endpoints)) as app:
                app.serve_forever()
                print(f"Satellite listening on http://{host}:{port}")
        except KeyboardInterrupt:
            print('\u001b[0m')  # Reset terminal text color.
            app.server_close()
