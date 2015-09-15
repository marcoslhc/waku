class BaseException(Exception):

    def __init__(self, message=None, code=None, original_exception=None):
        self.message = message or 'Template does not exists'
        self.code = code or '0'
        self.original_exception = original_exception or original_exception

    def __str__(self):
        return "%s: %s. Code: %s\n%s" % (self.__class__,
                                         self.message,
                                         self.code,
                                         self.original_exception.__str__())
