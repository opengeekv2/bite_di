from inspect import getfullargspec, ismethod, isawaitable
from functools import wraps

def _replace_args_by_string(args: tuple, argspec: list[str], contents: dict) -> tuple:
    arglist = list(args)
    for i, arg in enumerate(argspec):
        parameter_to_inject = contents.get(arg, None)
        if parameter_to_inject is not None and i >= len(arglist):
            arglist.append(parameter_to_inject)
    return (arglist)

def _replace_kwargs(kwargs: dict, contents: dict):
    for k, v in kwargs.items():
        if v is None and contents.get(k, None) is not None:
            kwargs[k] = contents[k]
    return kwargs

def create_container():
    def container(new: dict={}, contents: dict={}):
        if new:
            contents.update(new)

        def dump():
            print(contents)
        
        def dec_inject(func):
            @wraps(func)
            def wrapper(*args, **kwargs):
                argspec = getfullargspec(func).args
                args = _replace_args_by_string(args, argspec, contents)
                kwargs = _replace_kwargs(kwargs, contents)
                
                return func(*args, **kwargs)
            
            return wrapper
        
        return dec_inject, dump
    return container

