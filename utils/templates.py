import os
from jinja2 import Template
from middleware.registerRequest import get_request


def render(template, **vars):
    if isinstance(template, basestring):
        filename = os.path.abspath(os.path.relpath(template))
        template_file = open(filename, 'r')
        template_string = template_file.read()
        template_file.close()
        template = Template(template_string)
    vars.setdefault('request', get_request())
    return template.render(**vars)
