from urllib.parse import parse_qs
from .downlink import Downlink
from .houston import Houston
from .uplink import Method, Uplink


def server(endpoints):
    def inner(environ, start_response):
        try:
            handler, query = match(environ, endpoints)
            downlink = handler(Uplink(environ, query), Downlink())
        except Houston as e:
            downlink = e.downlink
            print(str(e))

        start_response(downlink.status, downlink.headers)

        return downlink

    return inner


def match(environ, endpoints):
    method = Method[environ['REQUEST_METHOD']]
    path = environ['PATH_INFO']
    path = path[:-1] if path.endswith('/') and path != "/" else path

    for (mode, route, handler) in endpoints:
        keys = route.split('/')[1:]
        values = path.split('/')[1:]

        if method == mode and len(keys) == len(values):
            params = parse_qs(environ['QUERY_STRING'])
            query = {key: value[0] for key, value in params.items()}

            for i, key in enumerate(keys):
                if key.startswith('[') and key.endswith(']'):
                    query[key[1:-1]] = values[i]

                elif key != values[i]:
                    break

                if i == len(keys) - 1:
                    return (handler, query)
            else:
                break

            continue

    raise Houston("This route is not handled!")
