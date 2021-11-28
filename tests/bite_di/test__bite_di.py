import pytest
from bite_di import container, inject
from bite_di.di import create_container

def test_container_not_recreated_after_import() -> None:
    from bite_di import container as c1
    assert c1 == container

def test_container_not_recreated_after_create_container() -> None:
    from bite_di import container as c1, create_container
    assert c1 != create_container()
    assert c1 == container

def test_container_not_recreated_after_create_container() -> None:
    from bite_di import container as c1, create_container
    assert c1 != create_container()
    assert c1 == container

def test_replaces_function_args_for_container_string_keys_value() -> None:
    HOLA = 'hola'
    contents = {
        'greeting': HOLA
    }
    container(contents)

    @inject
    def greet(greeting: str):
        return greeting

    assert HOLA == greet()

falsy_values_except_none = [
        [], (), {}, set(), '', b'', range(0), 0b0, 0x0, 00, 0, 0.0, 0j, False
]

@pytest.mark.parametrize('param', falsy_values_except_none)    
def test_replaces_function_args_for_container_falsy_values_except_none(param) -> None:
    
    contents = {
        'param': param
    }

    container(contents)

    @inject
    def greet(param):
        return param

    assert param == greet()

def test_does_not_replace_none_container_values() -> None:
    contents = {
        'param': None
    }

    container(contents)

    @inject
    def greet(param):
        return param

    with pytest.raises(TypeError):
        greet()


def test_not_replaces_function_args_when_passed() -> None:
    HOLA = 'hola'
    HELLO = 'hello'
    NAME = 'John Cleese'
    contents = {
        'greeting': HOLA,
        'name': NAME
    }
    container(contents)

    @inject
    def greet(greeting: str, name: str):
        return '{} {}'.format(greeting, name)

    assert (HELLO + ' ' + NAME) == greet(HELLO)

def test_replaces_function_with_default_args() -> None:
    HOLA = 'hola'
    HELLO = 'hello'
    NAME = 'John Cleese'
    OTHER_NAME = 'Eric Idle'
    contents = {
        'greeting': HOLA,
        'name': NAME
    }
    container(contents)

    @inject
    def greet(greeting: str = HELLO, name: str = OTHER_NAME):
        return '{} {}'.format(greeting, name)

    assert (HOLA + ' ' + NAME) == greet()

def test_replaces_none_kwargs_with_ones_in_container() -> None:
    HOLA = 'hola'
    NAME = 'John Cleese'
    contents = {
        'greeting': HOLA,
        'name': NAME
    }
    container(contents)

    @inject
    def greet(**kwargs):
        greeting = kwargs['greeting']
        name = kwargs['name']
        return '{} {}'.format(greeting, name)

    assert (HOLA + ' ' + NAME) == greet(greeting=None, name=None)

def test_not_replaces_provided_kwargs_with_ones_in_container() -> None:
    HOLA = 'hola'
    HELLO = 'hello'
    NAME = 'John Cleese'
    OTHER_NAME = 'Eric Idle'
    contents = {
        'greeting': HOLA,
        'name': NAME
    }
    container(contents)

    @inject
    def greet(**kwargs):
        greeting = kwargs['greeting']
        name = kwargs['name']
        return '{} {}'.format(greeting, name)

    assert (HELLO + ' ' + OTHER_NAME) == greet(greeting=HELLO, name=OTHER_NAME)
    assert (HELLO + ' ' + NAME) == greet(greeting=HELLO, name=None)
    assert (HOLA + ' ' + OTHER_NAME) == greet(greeting=None, name=OTHER_NAME)

@pytest.mark.parametrize('param', falsy_values_except_none)    
def test_replaces_function_kwargs_for_container_falsy_values_except_none(param) -> None:
    
    contents = {
        'key': param
    }

    container(contents)

    @inject
    def greet(**kwargs):
        return kwargs['key']

    assert param == greet(key=None)

def test_replaces_args_and_kwargs() -> None:
    HOLA = 'hola'
    HELLO = 'hello'
    NAME = 'John Cleese'
    OTHER_NAME = 'Eric Idle'
    contents = {
        'greeting': HOLA,
        'name': NAME,
    }
    container(contents)

    @inject
    def greet(greeting, name, **kwargs):
        other_greeting = kwargs['other_greeting']
        other_name = kwargs['other_name']
        return '{} {} {} {}'.format(greeting, name, other_greeting, other_name)

    assert (HOLA + ' ' + NAME + ' ' + HELLO + ' ' + OTHER_NAME
        == greet(HOLA, NAME, other_greeting=HELLO, other_name=OTHER_NAME))
class Prova:
    @inject
    def __init__(self, param):
        self.param = param
        
    @inject
    def prova(self, param):
        return param

    @inject
    def prova_self(self, param):
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

def test_container_dump(capsys):
    container = create_container()
    contents = {
        'greeting': 'hola'
    }
    inject, dump = container(contents)
    dump()
    captured = capsys.readouterr()
    assert captured.out == "{'greeting': 'hola'}\n"
