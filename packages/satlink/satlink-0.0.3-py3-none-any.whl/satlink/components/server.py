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
    values = path.split('/')[1:]
    params = parse_qs(environ['QUERY_STRING'])
    query = {k: v[0] for k, v in params.items()}

    endpoints = [
        (m, r, h, r.split('/')[1:]) 
        for (m, r, h) in endpoints
        if m == method and len(r.split('/')[1:]) == len(values)
    ]

    matches = endpoints.copy()

    for i, value in enumerate(values):
        for (m, r, h, k) in endpoints:
            if k[i].startswith('[') and k[i].endswith(']'):
                exact = [
                    (m, r, h, k) 
                    for (m, r, h, k) in endpoints
                    if (k[i] == value)
                ]

                if (len(exact) > 0):
                    matches.remove((m, r, h, k))
                else:
                    query[r[2:-1]] = value

            elif k[i] != value:
                matches.remove((m, r, h, k))

    if (len(matches) > 0):
        return (matches[0][2], query)

    raise Houston("This route is not handled!")

"""
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
"""
