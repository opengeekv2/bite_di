from inspect import getfullargspec, signature, Parameter, Signature
from functools import wraps
from typing import Callable, List, Dict, Tuple, Any


def _replace_args_by_string(
        args: Tuple[Any, ...], kwargs: Dict[str, Any], argspec: List[str],
        contents: Dict[str, Any]) -> tuple:
    arglist = list(args)
    for i, arg in enumerate(argspec):
        if arg not in kwargs.keys():
            parameter_to_inject = contents.get(arg, None)
            if parameter_to_inject is not None and i >= len(arglist):
                arglist.append(parameter_to_inject)
    return tuple(arglist)


def _merge_varargs(
        args: Tuple[Any, ...], varargs: str,
        contents: Dict[str, Any]) -> tuple:
    return args + contents.get(varargs, ())


def _replace_kwonlyargs(
        kwargs: Dict[str, Any], kwonlyargs: List[str],
        contents: Dict[str, Any]) -> Dict[str, Any]:
    for kwonlyarg in kwonlyargs:
        if kwonlyarg not in kwargs.keys():
            parameter_to_inject = contents.get(kwonlyarg, None)
            if parameter_to_inject is not None:
                kwargs[kwonlyarg] = parameter_to_inject
    return kwargs


def _merge_named_kwargs(
        kwargs: Dict[str, Any], varkw: str,
        contents: Dict[str, Any]) -> Dict[str, Any]:
    kwargs.update(contents.get(varkw, {}).copy())
    return kwargs


def _replace_kwargs(
        kwargs: Dict[str, Any], kwonlyargs: List[str],
        contents: Dict[str, Any]) -> Dict[str, Any]:
    for k, v in kwargs.items():
        if v is None and k not in kwonlyargs and contents.get(
                k, None) is not None:
            kwargs[k] = contents[k]
    return kwargs


def create_container() -> Callable:
    def container(
            new: Dict[str, Any] = {}, contents: Dict[str, Any] = {},
            decorated: List = [Callable]) -> Callable:
        if new:
            contents.update(new)

        def dump() -> None:
            print(contents)

        def inject(func: Callable) -> Callable:
            decorated.append(func)

            @wraps(func)
            def wrapper(*args: Any, **kwargs: Dict[str, Any]) -> Any:
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

            def generate_test_call(self, f: Callable) -> str:
                s = signature(f)
                call_signature = s.replace()
                for p in s.parameters.values():
                    call_signature = s.replace(
                        parameters=[p.replace(annotation=Parameter.empty)],
                        return_annotation=Signature.empty)
                call = str(call_signature)
                for key in s.parameters.keys():
                    call.replace(key, str(contents.get(key)))
                return f.__name__ + call

        return Container(inject, dump, decorated)
    return container
