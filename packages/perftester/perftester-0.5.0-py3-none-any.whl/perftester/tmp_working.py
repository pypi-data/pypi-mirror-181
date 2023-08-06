class Value:
    def __init__(self, value):
        self.result = value

    def __call__(self):
        return self.result
    
    def __gt__(self, other):
        return other(self.result)


class Do:
    def __init__(self, func=None, *args, **kwargs):
        self.func = func
        self.args = args
        self.kwargs = kwargs
    
    def __call__(self, *add_args, **add_kwargs):
        these_args = {**self.kwargs, **add_kwargs}
        self.result = self.func(*add_args, *self.args, **these_args)
        return self.result
    
    def __gt__(self, other):
        try:
            return other(self.__call__())
        except:
            return other(self.result)


double = lambda x: 2 * x
square = lambda x: x ** 2
add = lambda x, y: x + y

Value(10) > Do(double) > Do(square) > Do(add, 50) > Do(print)
