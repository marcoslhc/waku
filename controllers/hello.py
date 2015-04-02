from utils.templates import render


class Hello(object):
    def __init__(self, req):
        self.request = req

    def post(self):
        vars = {key: value for key, value in self.request.params.iteritems()}
        return render('templates/hello/index.html', **vars)

    def get(self):
        return render('templates/hello/form.html')


