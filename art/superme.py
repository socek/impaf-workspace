

import inspect


def get_class_that_defined_method(meth):
    if inspect.ismethod(meth):
        for cls in inspect.getmro(meth.__self__.__class__):
            if cls.__dict__.get(meth.__name__) is meth:
                return cls
        meth = meth.__func__ # fallback to __qualname__ parsing
    if inspect.isfunction(meth):
        cls = getattr(inspect.getmodule(meth),
                      meth.__qualname__.split('.<locals>', 1)[0].rsplit('.', 1)[0])
        if isinstance(cls, type):
            return cls
    return None

def superme(fun):
    superfun = getattr(fun, '_myfun', fun)
    cls = get_class_that_defined_method(superfun)
    print('z', cls)

    def wrapper(self, *args, **kwargs):
        print('wrap')
        return fun(self, *args, **kwargs)
    wrapper._myfun = fun
    # print(wrapper.__name__, id(wrapper), id(wrapper._myfun), wrapper)
    # print(fun.__name__, id(fun), getattr(fun, '_myfun', None), fun)
    return wrapper


class One(object):

    def elo(self):
        print('elo')


class Two(One):

    @superme
    def elo(self):
        print('Two')


class Three(Two):

    @superme
    def elo(self):
        print('Three')


class Four(Three):

    @superme
    def elo(self):
        print('Four')


Four().elo()
