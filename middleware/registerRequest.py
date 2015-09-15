from webob import Request
from threading import local


class Localized(object):

    def __init__(self):
        self.local = local()

    def register(self, object):
        self.local.object = object

    def unregister(self):
        del self.local.object

    def __call__(self):
        try:
            return self.local.object
        except AttributeError:
            raise TypeError("No object has been assigned to this thread")


get_request = Localized()


class RegisterRequest(object):

    def __init__(self, app):
        self.app = app

    def __call__(self, environ, start_response):
        req = Request(environ)
        get_request.register(req)
        try:
            return self.app(environ, start_response)
        finally:
            get_request.unregister()
