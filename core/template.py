import os
from jinja2 import Template as _Template
from middleware.registerRequest import get_request
import core.exception
import settings


class NotSuchTemplateFileException(core.exception.BaseException):
    pass


class Template(object):

    def __init__(self, template=None, context=None):
        self.context = context
        if isinstance(template, basestring):
            template_file = self.get_template_file(template)
            self.template = _Template(template_file)

    def render(self, newContext=None):
        if self.context is not None:
            self.context.setdefault('request', get_request())
            if newContext is not None:
                self.context.update(newContext)
        return self.template.render(self.context)

    def get_template_file(self, template):
        if not template.startswith('/'):
            template = '/%s' % (template, )
        try:
            filename = os.path.abspath(settings.TEMPLATE_DIR + template)
            output = open(filename, 'r').read()
        except Exception as e:
            raise NotSuchTemplateFileException(original_exception=e)
        return output
