from utils.templates import render
from core.router import Router
from core.controller import rest_controller
from controllers.hello import Hello


middleware = (
    'middleware.authRequest.AuthRequest',
    'middleware.registerRequest.RegisterRequest',
    'middleware.cors.CORSRequest',

)


def applyMiddleware(app):
    modules = [('.'.join(module.split('.')[:-1]),
                '.'.join(module.split('.')[-1:])) for module in middleware]
    for module, f in modules:
        module = __import__(module, fromlist=[f])
        app = getattr(module, f)(app)
    return app


hello_world = Router()
hello_world.add_route('/hello/{name:\w*}', controller=Hello)
hello_world = applyMiddleware(hello_world)

if __name__ == '__main__':
    import doctest
    from wsgiref.simple_server import make_server

    doctest.testmod()
    print 'serving'
    server = make_server('127.0.0.1', 8080, hello_world)
    server.serve_forever()
