from webob import Request, Response
from utils.templates import render


def error401():
    status = 401
    body = render('templates/error/401.html')
    return Response(status=status, headers={
        'WWW-Authenticate': 'Basic realm="this realm"'
    }, body=body)


class AuthRequest(object):
    def __init__(self, app):
        self.app = app

    def __call__(self, environ, start_response):
        req = Request(environ)
        if not self.authorized(req.headers.get('authorization')):
            resp = self.auth_required(req)
        else:
            resp = self.app
        return resp(environ, start_response)

    def authorized(self, header):
        dir(header)
        if not header:
            return False
        auth_type, encoded = header.split(None, 1)
        if not auth_type.lower() == 'basic':
            return False
        username, password = encoded.decode('base64').split(':', 1)
        return self.check_password(username, password)

    def check_password(self, username, password):
        return username == password

    def auth_required(self, req):
        return error401()
