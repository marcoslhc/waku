from utils.templates import render
from formencode.variabledecode import variable_decode


class Hello(object):
    def __init__(self, req):
        self.request = req

    def post(self):
        vars = variable_decode(self.request.params)
        print(vars)
        return render('templates/hello/index.html', **vars)

    def get(self):
        return render('templates/hello/form.html')
