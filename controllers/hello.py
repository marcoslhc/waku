from formencode.variabledecode import variable_decode
from core.template import Template
from core.controller import rest_controller


@rest_controller
class Hello(object):
    kwargs = {}

    def __init__(self, req, *args, **kwargs):
        self.request = req
        post_vars = variable_decode(self.request.params)
        url_vars = variable_decode(self.request.urlvars)
        self.kwargs = kwargs.copy()
        self.kwargs.update(url_vars)
        self.kwargs.update(post_vars)

    def post(self):
        return Template('templates/hello/index.html', self.kwargs).render()

    def get(self):
        return Template('templates/hello/form.html', self.kwargs).render()
