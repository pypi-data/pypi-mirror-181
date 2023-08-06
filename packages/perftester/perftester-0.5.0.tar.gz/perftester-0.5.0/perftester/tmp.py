from pprint import pprint


class Container:
    def __init__(self, values):
        self.values = values

    def __gt__(self, other):
        return Container(type(self.values)(other(i) for i in self.values))


class Show:
    def __call__(self, obj=None, func=None, *args, **kwargs):
        self.obj = obj
        if not func:
            pprint(obj.result)    
        else:
            pprint(func(obj.result, *args, **kwargs))
        return obj
    
    def __gt__(self, other):
        return other(self.obj.result)



class Value:
    def __init__(self, value):
        self.result = value

    def __call__(self):
        return self.result
    
    def __gt__(self, other):
        return other(self.result)


class Do:
    def __init__(self, func, *args, parallel=False, **kwargs):
        self.func = func
        self.args = args
        self.kwargs = kwargs
        self.result = None
        self.parallel = parallel
    
    def __call__(self, *add_args, **add_kwargs):
        these_args = {**self.kwargs, **add_kwargs}
        self.result = self.func(*add_args, *self.args, **these_args)
        return self.result
    
    def __gt__(self, other):
        if isinstance(other, Show):
            return other(self)
        try:
            return other(self.__call__())
        except:
            return other(self.result)
    


double = lambda x: 2 * x
square = lambda x: x ** 2
add = lambda x, y: x + y

Value(10) > Do(double) > Show() > Do(double) > Show()

Value(10) > Do(double) > Do(square) > Do(add, 50) > Do(print)
Value(10) > Do(double) > Do(square) > Show() > Do(add, 50) > Show()

Container([1, 2, 3]) > Do(double) > Show()