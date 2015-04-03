from webob import Request, Response


allowed_hosts = ('*')
allowed_methods = ('GET', 'POST', 'PUT', 'DELETE', 'HEAD', 'OPTIONS')
allowed_headers = [
    ('Access-Control-Allow-Origin', ''),
    ('Access-Control-Max-Age', ''),
    ('Access-Control-Allow-Credentials', ''),
    ('Access-Control-Allow-Methods', ''),
    ('Access-Control-Allow-Headers', ''),
    ('Access-Control-Allow-Credentials', '')
]


class InvalidHeaderException(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)


class CORSRequest(object):
    def __init__(self, app):
        self.app = app

    def setHeader(self, headers, header, value):
        valheader = zip(*allowed_headers)[0]

        try:
            valheader.index(header)
        except (ValueError):
            raise InvalidHeaderException(valheader)

        headers.append((header, value))
        return (header, value)

    def validateMethod(self, method):
        return (method in methods and method) or False

    def validateOrigin(self, origin):
        return ('*' in allowed_hosts or origin in allowed_hosts) \
            and origin \
            or False

    def __call__(self, environ, start_response):
        req = Request(environ)

        if not self.validateMethod(req.method):
            return Response(status=405)

        if req.method in ('OPTIONS', 'HEAD'):
            return Response(status=204)

        def custom_start_response(status, headers, exc_info=None):
            self.setHeader(headers, 'Access-Control-Allow-Methods',
                           ','.join(methods))
            self.setHeader(headers, 'Access-Control-Allow-Credentials',
                           'True')
            self.setHeader(headers, 'Access-Control-Allow-Origin',
                           self.validateOrigin(req.host_url))
            return start_response(status, headers, exc_info)

        return self.app(environ, custom_start_response)
