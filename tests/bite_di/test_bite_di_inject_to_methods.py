from bite_di import container, inject


class Prova:  # noqa: H601
    @inject
    def __init__(self, param: str):
        self.param = param

    @inject
    def prova(self, param: str) -> str:
        return param

    @inject
    def prova_self(self, param: str):
        return self


def test_replace_provided_args_in_method():
    HOLA = 'hola'

    contents = {
        'param': HOLA
    }
    container(contents)

    prova = Prova()
    assert HOLA == prova.prova()


def test_not_replace_provided_args_in_method():
    HOLA = 'hola'
    HELLO = 'hello'

    contents = {
        'param': HOLA
    }
    container(contents)

    prova = Prova()
    assert HELLO == prova.prova(HELLO)


def test_not_replace_self_in_method():
    HOLA = 'hola'

    contents = {
        'self': HOLA
    }
    container(contents)

    prova = Prova()
    assert prova == prova.prova_self(HOLA)


def test_replace_provided_args_in_init():
    HOLA = 'hola'

    contents = {
        'param': HOLA
    }
    container(contents)

    prova = Prova()
    assert HOLA == prova.param
