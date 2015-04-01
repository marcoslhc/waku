import urllib
from middleware.registerRequest import get_request


def url(*segments, **vars):
    base_url = get_request().application_url
    path = '/'.join(str(s) for s in segments)
    if not path.startswith('/'):
        path = '/' + path
    if vars:
        path += '?' + urllib.urlencode(vars)
    return base_url + path
