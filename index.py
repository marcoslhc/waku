from utils.templates import render
from core.router import Router
from core.controller import rest_controller
from middleware.registerRequest import RegisterRequest
from middleware.authRequest import AuthRequest


class Hello(object):
    def __init__(self, req):
        self.request = req

    def post(self):
        vars = {key: value for key, value in self.request.params.iteritems()}
        return render('templates/hello/index.html', **vars)

    def get(self):
        return render('templates/hello/form.html')


hello = rest_controller(Hello)
hello_world = Router()
hello_world.add_route('/', controller=hello)
hello_world = AuthRequest(hello_world)
hello_world = RegisterRequest(hello_world)

if __name__ == '__main__':
    import doctest
    from wsgiref.simple_server import make_server

    doctest.testmod()
    print 'serving'
    server = make_server('127.0.0.1', 8080, hello_world)
    server.serve_forever()
