from webob import Request
from webob import exc
import re
import sys

var_regex = re.compile(r'''
        \{                # The exact character "{"
        (\w+)             # The variable name restricted to a-zA-Z0-9
        (?::([^}]+))?     # The optional :regex part
        \}                # The exact character "}"
        ''', re.VERBOSE)


class Router(object):
    def __init__(self):
        self.routes = []

    def add_route(self, template, controller, **vars):
        if isinstance(controller, basestring):
            controller = load_controller(controller)
        self.routes.append((re.compile(template_to_regex(template)),
                            controller, vars))

    def __call__(self, environ, start_response):
        req = Request(environ)
        for regex, controller, vars in self.routes:
            match = regex.match(req.path_info)
            if match:
                req.urlvars = match.groupdict()
                req.urlvars.update(vars)
                return controller(environ, start_response)
            return exc.HTTPNotFound()(environ, start_response)


def load_controller(string):
    module_name, func_name = string.split(':', 1)
    __import__(module_name)
    module = sys.modules[module_name]
    func = getattr(module, func_name)
    return func


def template_to_regex(template):
    """ Converts a string formated as {var_name[:regex]} as a valid route

    >>> print template_to_regex('/a/static/path')
    ^\/a\/static\/path$
    >>> print template_to_regex('/{year:\d\d\d\d}/')
    ^\/(?P<year>\d\d\d\d)\/$
    """

    regex = ''
    last_pos = 0
    for match in var_regex.finditer(template):
        regex += re.escape(template[last_pos:match.start()])
        var_name = match.group(1)
        expr = match.group(2) or '[^/]+'
        expr = '(?P<%s>%s)' % (var_name, expr)
        regex += expr
        last_pos = match.end()
    regex += re.escape(template[last_pos:])
    regex = '^%s$' % regex
    return regex
