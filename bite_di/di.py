from inspect import getfullargspec
from functools import wraps
from typing import Callable, List, Dict, Mapping, Any, MutableMapping
from typing import Tuple, cast, TypeVar
import typing


def _none_function() -> None:
    return None


F = TypeVar('F', bound=Callable[..., object])


class Container:  # noqa: H601

    def __replace_args_by_string(
        self,
        args: Tuple[object, ...], kwargs: Dict[str, object],
        argspec: List[str]
    ) -> Tuple[object, ...]:
        arglist = list(args)
        n_args = len(arglist)
        for i, arg in enumerate(argspec):
            if arg not in kwargs.keys():
                parameter_to_inject = self.__contents.get(arg, _none_function)
                if parameter_to_inject() is not None and i >= n_args:
                    arglist.append(parameter_to_inject())
        return tuple(arglist)

    def __merge_varargs(
        self, args: Tuple[object, ...], varargs: str,
            ) -> Tuple[object, ...]:
        return args + cast(
            Tuple[object, ...],
            self.__contents.get(varargs, _none_function)()
        )

    def __replace_kwonlyargs(
            self,
            kwargs: Dict[str, object], kwonlyargs: List[str],
            ) -> Dict[str, object]:
        for kwonlyarg in kwonlyargs:
            if kwonlyarg not in kwargs.keys():
                parameter_to_inject = self.__contents.get(
                    kwonlyarg, _none_function
                )()
                if parameter_to_inject is not None:
                    kwargs[kwonlyarg] = parameter_to_inject
        return kwargs

    def __merge_named_kwargs(
            self,
            kwargs: Dict[str, object], varkw: str
            ) -> Dict[str, object]:
        parameter_to_inject = self.__contents.get(varkw, _none_function)()
        if parameter_to_inject is not None:
            kwargs.update(cast(Dict[str, object], parameter_to_inject).copy())
        return kwargs

    def __replace_kwargs(
        self, kwargs: Dict[str, object], kwonlyargs: List[str]
            ) -> Dict[str, object]:
        for k, v in kwargs.items():
            if v is None and k not in kwonlyargs and self.__contents.get(
                    k, _none_function)() is not None:
                kwargs[k] = self.__contents[k]()
        return kwargs

    def __from_var_dict(self, vardict: Mapping[str, object]) -> None:
        self.__contents.update(
            dict(map(lambda x: (x[0], lambda: x[1]), vardict.items()))
        )

    def __init__(self) -> None:
        self.__contents: MutableMapping[str, Callable[[], object]] = {}
        self.decorated: List[Callable[..., object]] = []

    def __call__(
            self, new: typing.Optional[Mapping[str, object] | Callable] = None,
            ) -> Callable[[F], F]:

        if new and isinstance(new, Dict):
            self.__from_var_dict(new)

        def inject(func: F) -> F:
            self.decorated.append(func)

            @wraps(func)
            def wrapper(*args: object, **kwargs: object) -> object:
                fullargspec = getfullargspec(func)
                args = self.__replace_args_by_string(
                    args, kwargs, fullargspec.args)
                if fullargspec.varargs is not None:
                    args = self.__merge_varargs(
                        args, fullargspec.varargs
                    )
                if fullargspec.varkw is not None:
                    kwargs = self.__merge_named_kwargs(
                        kwargs, fullargspec.varkw)
                kwargs = self.__replace_kwonlyargs(
                    kwargs, fullargspec.kwonlyargs)
                kwargs = self.__replace_kwargs(
                    kwargs, fullargspec.kwonlyargs)

                return func(*args, **kwargs)

            return cast('F', wrapper)

        def add_dependency(key: str, factory: Callable):
            self.add_factory(key, factory)

        if new and callable(new):
            new(add_dependency)

        return inject

    def dump(self) -> None:
        print(dict(map(
            lambda item: (item[0], item[1]()),
            self.__contents.items()
        )))

    def get(self, key: str) -> Any:
        return self.__contents.get(key, _none_function)()

    def add_var(self, key: str, var: object) -> None:
        def wrapper() -> object:
            return var
        self.__contents[key] = wrapper

    def add_factory(self, key: str, c: Callable[[], object]) -> None:
        self.__contents[key] = c
