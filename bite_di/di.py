from inspect import getfullargspec
from functools import wraps
from typing import Callable, List, Dict, Tuple, cast


def _replace_args_by_string(
        args: Tuple[object, ...], kwargs: Dict[str, object],
        argspec: List[str], contents: Dict[str, object]) -> tuple:
    arglist = list(args)
    for i, arg in enumerate(argspec):
        if arg not in kwargs.keys():
            parameter_to_inject = contents.get(arg, None)
            if parameter_to_inject is not None and i >= len(arglist):
                arglist.append(parameter_to_inject)
    return tuple(arglist)


def _merge_varargs(
        args: Tuple[object, ...], varargs: str,
        contents: Dict[str, object]) -> tuple:
    return args + cast(Tuple[object, ...], contents.get(varargs, ()))


def _replace_kwonlyargs(
        kwargs: Dict[str, object], kwonlyargs: List[str],
        contents: Dict[str, object]) -> Dict[str, object]:
    for kwonlyarg in kwonlyargs:
        if kwonlyarg not in kwargs.keys():
            parameter_to_inject = contents.get(kwonlyarg, None)
            if parameter_to_inject is not None:
                kwargs[kwonlyarg] = parameter_to_inject
    return kwargs


def _merge_named_kwargs(
        kwargs: Dict[str, object], varkw: str,
        contents: Dict[str, object]) -> Dict[str, object]:
    kwargs.update(cast(Dict[str, object], contents.get(varkw, {})).copy())
    return kwargs


def _replace_kwargs(
        kwargs: Dict[str, object], kwonlyargs: List[str],
        contents: Dict[str, object]) -> Dict[str, object]:
    for k, v in kwargs.items():
        if v is None and k not in kwonlyargs and contents.get(
                k, None) is not None:
            kwargs[k] = contents[k]
    return kwargs


def create_container() -> Callable:
    def container(
            new: Dict[str, object] = {}, contents: Dict[str, object] = {},
            decorated: List = [Callable]) -> Callable:
        if new:
            contents.update(new)

        def dump() -> None:
            print(contents)

        def inject(func: Callable) -> Callable:
            decorated.append(func)

            @wraps(func)
            def wrapper(*args: object, **kwargs: object) -> object:
                fullargspec = getfullargspec(func)
                args = _replace_args_by_string(
                    args, kwargs, fullargspec.args, contents)
                if fullargspec.varargs is not None:
                    args = _merge_varargs(args, fullargspec.varargs, contents)
                if fullargspec.varkw is not None:
                    kwargs = _merge_named_kwargs(
                        kwargs, fullargspec.varkw, contents)
                kwargs = _replace_kwonlyargs(
                    kwargs, fullargspec.kwonlyargs, contents)
                kwargs = _replace_kwargs(
                    kwargs, fullargspec.kwonlyargs, contents)

                return func(*args, **kwargs)

            return wrapper

        class Container:
            def __init__(
                self,
                inject: Callable,
                dump: Callable,
                decorated: list
            ):
                self.inject = inject
                self.dump = dump
                self.decorated = decorated

            def __call__(self) -> Tuple[Callable, Callable]:
                return (self.inject, self.dump)

        return Container(inject, dump, decorated)
    return container
