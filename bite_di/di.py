from inspect import getfullargspec
from functools import wraps

def _replace_args_by_string(args: tuple, kwargs: dict, argspec: list[str], contents: dict) -> tuple:
    arglist = list(args)
    for i, arg in enumerate(argspec):
        if arg not in kwargs.keys():
            parameter_to_inject = contents.get(arg, None)
            if parameter_to_inject is not None and i >= len(arglist):
                arglist.append(parameter_to_inject)
    return tuple(arglist)

def _merge_varargs(args: tuple, varargs: str, contents: dict) -> tuple:
    return args + contents.get(varargs, ())

def _replace_kwonlyargs(kwargs: dict, kwonlyargs: list[str], contents: dict) -> dict:
    for kwonlyarg in kwonlyargs:
        if kwonlyarg not in kwargs.keys():
            parameter_to_inject = contents.get(kwonlyarg, None)
            if parameter_to_inject is not None:
                kwargs[kwonlyarg] = parameter_to_inject
    return kwargs

def _merge_named_kwargs(kwargs: dict, varkw: str, contents: dict) -> dict:
    kwargs.update(contents.get(varkw, {}).copy())
    return kwargs

def _replace_kwargs(kwargs: dict, kwonlyargs: list[str], contents: dict) -> dict:
    for k, v in kwargs.items():
        if v is None and k not in kwonlyargs and contents.get(k, None) is not None:
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
                fullargspec = getfullargspec(func)
                args = _replace_args_by_string(args, kwargs, fullargspec.args, contents)
                args = _merge_varargs(args, fullargspec.varargs, contents)
                kwargs = _merge_named_kwargs(kwargs, fullargspec.varkw, contents)
                kwargs = _replace_kwonlyargs(kwargs, fullargspec.kwonlyargs, contents)
                kwargs = _replace_kwargs(kwargs, fullargspec.kwonlyargs, contents)

                return func(*args, **kwargs)
            
            return wrapper
        
        return dec_inject, dump
    return container

