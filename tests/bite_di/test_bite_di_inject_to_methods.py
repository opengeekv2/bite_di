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


def test_replace_provided_args_in_init():
    HOLA = 'hola'

    contents = Contents()
    contents.from_var_dict({
        'param': HOLA
    })
    container(contents)

    prova = Prova()
    assert HOLA == prova.param
