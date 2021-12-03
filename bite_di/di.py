from inspect import getfullargspec
from functools import wraps
from typing import Callable, List, Dict, DefaultDict
from typing import Mapping, Tuple, cast, TypeVar, Any


class Contents(DefaultDict[str, Callable[[], Any]]):  # noqa: H601
    def from_var_dict(self, vardict: Dict[str, Any]) -> None:
        self.update(dict(map(lambda x: (x[0], lambda: x[1]), vardict.items())))

    def add_var(self, key: str, var: Any) -> None:
        def wrapper():
            return var
        self[key] = wrapper

    def add_factory(self, key: str, c: Callable[[], Any]) -> None:
        self[key] = c


def _replace_args_by_string(
        args: Tuple[object, ...], kwargs: Dict[str, object],
        argspec: List[str], contents: Dict[str, Callable[[], Any]] = {}
        ) -> Tuple[object, ...]:
    arglist = list(args)
    n_args = len(arglist)
    for i, arg in enumerate(argspec):
        if arg not in kwargs.keys():
            parameter_to_inject = contents.get(arg, lambda: None)
            if parameter_to_inject() is not None and i >= n_args:
                arglist.append(parameter_to_inject())
    return tuple(arglist)


def _merge_varargs(
        args: Tuple[object, ...], varargs: str,
        contents: Dict[str, Callable[[], Any]] = {}) -> Tuple[object, ...]:
    return args + cast(
        Tuple[object, ...],
        contents.get(varargs, lambda: None)()
    )


def _replace_kwonlyargs(
        kwargs: Dict[str, object], kwonlyargs: List[str],
        contents: Dict[str, Callable[[], Any]] = {}) -> Dict[str, object]:
    for kwonlyarg in kwonlyargs:
        if kwonlyarg not in kwargs.keys():
            parameter_to_inject = contents.get(kwonlyarg, lambda: None)()
            if parameter_to_inject is not None:
                kwargs[kwonlyarg] = parameter_to_inject
    return kwargs


def _merge_named_kwargs(
        kwargs: Dict[str, object], varkw: str,
        contents: Dict[str, Callable[[], Any]]) -> Dict[str, object]:
    parameter_to_inject = contents.get(varkw, lambda: None)()
    if parameter_to_inject is not None:
        kwargs.update(cast(Dict[str, object], parameter_to_inject).copy())
    return kwargs


def _replace_kwargs(
        kwargs: Dict[str, object], kwonlyargs: List[str],
        contents: Dict[str, Callable[[], Any]]) -> Dict[str, object]:
    for k, v in kwargs.items():
        if v is None and k not in kwonlyargs and contents.get(
                k, lambda: None)() is not None:
            kwargs[k] = contents[k]()
    return kwargs


F = TypeVar('F', bound=Callable[..., object])


class Container:

    def __init__(self) -> None:
        self.decorated: List[Callable[..., Any]] = []
        self.dump: Callable[[], None] = lambda: print()

    def __call__(
            self, new: Dict[str, Callable[[], Any]] = {},
            contents: Dict[str, Callable[[], Any]] = {},
            decorated: List[Callable[..., Any]] = []
            ) -> Tuple[
                Callable[[F], F],
                Callable[[], None]]:

        if new:
            contents.update(new)

        def dump() -> None:
            print(dict(map(
                lambda item: (item[0], item[1]()),
                contents.items()
            )))

        self.dump = dump

        def inject(func: F) -> F:
            f = cast(
                Callable[[List[object], Mapping['str', object]], object], func
            )
            decorated.append(f)

            @wraps(func)
            def wrapper(*args: object, **kwargs: object) -> object:
                fullargspec = getfullargspec(f)
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

            return cast('F', wrapper)
        return inject, dump


def create_container() -> Container:
    return Container()
