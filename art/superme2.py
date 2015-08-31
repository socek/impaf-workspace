def superme(fun):
    def wrapper(*args, **kwargs):
        return fun(*args, **kwargs)
    return wrapper


class One(object):

    @superme
    def method(self):
        pass


class Two(One):

    def method(self):
        print(super().method)

Two().method()
