from inspect import getfullargspec, ismethod, isawaitable
from functools import wraps

def _replace_args(args: tuple, argspec: list[str], contents: dict) -> tuple:
    arglist = list(args)
    for i, arg in enumerate(argspec):
        parameter_to_inject = contents.get(arg, None)
        if parameter_to_inject and i >= len(arglist):
            arglist.append(parameter_to_inject)
    return (arglist)


def create_container():
    def container(new: dict={}, contents: dict={}):
        if new:
            contents.update(new)
        
        def dec_inject(func):
            @wraps(func)
            def wrapper(*args, **kwargs):
                #to_inject = func
                #if ismethod(func):
                #    to_inject = func.__func__
                argspec = getfullargspec(func).args
                if len(argspec) == len(args):
                    return func(*args, **kwargs)
                args = _replace_args(args, argspec, contents)
                #if isawaitable(func):
                #    
                #    async def tmp():
                #        return (await func(*(arglist), **kwargs))
                #    
                #    return tmp()
                
                return func(*args, **kwargs)
            
            return wrapper
        
        return dec_inject
    return container

