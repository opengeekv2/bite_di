from bite_di import container, Contents, inject
from typing import Optional


class Prova:  # noqa: H601
    @inject
    def __init__(self, param: str = None):
        self.param = param

    @inject
    def prova(self, param: str = None) -> Optional[str]:
        return param

    @inject
    def prova_self(self, param: str):
        return self


def test_replace_provided_args_in_method():
    HOLA = 'hola'

    contents = Contents()
    contents.from_var_dict({
        'param': HOLA
    })
    print(contents)
    container(contents)

    prova = Prova()
    assert HOLA == prova.prova()


def test_not_replace_provided_args_in_method():
    HOLA = 'hola'
    HELLO = 'hello'

    contents = Contents()
    contents.from_var_dict({
        'param': HOLA
    })
    container(contents)

    prova = Prova()
    assert HELLO == prova.prova(HELLO)


def test_not_replace_self_in_method():
    HOLA = 'hola'

    contents = Contents()
    contents.from_var_dict({
        'self': HOLA
    })
    container(contents)

    prova = Prova()
    assert prova == prova.prova_self(HOLA)


class Service1:  # noqa: H601
    pass


class Service3:  # noqa: H601
    pass


class Service2:
    @inject
    def __init__(self, s3: Service3):
        self._s3 = s3


class Controller:
    @inject
    def __init__(self, s1: Service1, s2: Service2):
        self._s1 = s1
        self._s2 = s2


def test_build_object_graph():
    contents = Contents()
    contents.add_factory('c', Controller)
    contents.add_factory('s1', Service1)
    contents.add_factory('s2', Service2)
    contents.add_factory('s3', Service3)
    container(contents)

    @inject
    def app(c: Controller):
        return c

    assert app() != app()
