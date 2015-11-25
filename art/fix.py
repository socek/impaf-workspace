import inspect


def get_class_that_defined_method(meth):
    if inspect.ismethod(meth):
        for cls in inspect.getmro(meth.__self__.__class__):
            if cls.__dict__.get(meth.__name__) is meth:
                return cls
        meth = meth.__func__  # fallback to __qualname__ parsing
    if inspect.isfunction(meth):
        module = inspect.getmodule(meth)
        data = meth.__qualname__.split('.<locals>', 1)[0].rsplit('.', 1)[0]
        cls = getattr(module, data)
        if isinstance(cls, type):
            return cls
    return None


def superme(need_result=False, *parent_args, **parent_kwargs):
    def superme(fun):
        def wrapper(self, *args_from_wrapper, **kwargs_from_wrapper):
            actual_function = getattr(fun, '_parent_function', fun)
            cls = get_class_that_defined_method(actual_function)
            superobj = super(cls, self)
            parent = getattr(superobj, actual_function.__name__)
            args = parent_args or args_from_wrapper
            kwargs = parent_kwargs or kwargs_from_wrapper
            print(cls, parent, args, kwargs)
            result = parent(*args, **kwargs)
            if need_result:
                return fun(
                    self,
                    result,
                    *args_from_wrapper,
                    **kwargs_from_wrapper
                )
            else:
                return fun(
                    self,
                    *args_from_wrapper,
                    **kwargs_from_wrapper
                )
        wrapper._parent_function = fun
        return wrapper
    return superme


class One(object):

    def elo(self):
        print('One')
        return 190


class Two(One):

    @superme(True)
    def elo(self, result):
        print('Two', result)


class Three(Two):

    # @superme(False, 150)
    @superme()
    def elo(self, data=12):
        print('Three', data)


class Four(Three):

    @superme(data=13)
    def elo(self):
        print('Four')
