import os
import sys
import tempita
from middleware.registerRequest import get_request


def render(template, **vars):
    if isinstance(template, basestring):
        caller_location = sys._getframe(1).f_globals['__file__']
        filename = os.path.abspath(
            os.path.join(os.path.dirname(caller_location), template))
        template = tempita.HTMLTemplate.from_filename(filename)
    vars.setdefault('request', get_request())
    return template.substitute(vars)
