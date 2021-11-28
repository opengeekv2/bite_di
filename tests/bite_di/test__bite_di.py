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

def test_injects_varargs_by_key() -> None:
    HOLA = 'hola'
    NAME = 'John Cleese'
    contents = {
        'fullgreeting': (HOLA, NAME)
    }
    container(contents)

    @inject
    def greet(*fullgreeting):
        greeting, name = fullgreeting
        return '{} {}'.format(greeting, name)

    assert (HOLA + ' ' + NAME) == greet()

def test_injects_varargs_by_key() -> None:
    HOLA = 'hola'
    NAME = 'John Cleese'
    contents = {
        'fullgreeting': (HOLA, NAME)
    }
    container(contents)

    @inject
    def greet(*fullgreeting):
        greeting, name = fullgreeting
        return '{} {}'.format(greeting, name)

    assert (HOLA + ' ' + NAME) == greet()

def test_injects_varargs_by_key_but_are_merged_to_passed() -> None:
    HOLA = 'hola'
    NAME = 'John Cleese'
    contents = {
        'fullgreeting': tuple([NAME])
    }
    container(contents)

    @inject
    def greet(*fullgreeting):
        greeting, name = fullgreeting
        return '{} {}'.format(greeting, name)

    assert (HOLA + ' ' + NAME) == greet(HOLA)

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

def test_respects_passed_posiotional_or_keyword_args():
    HOLA = 'hola'
    NAME = 'John Cleese'
    OTHER_NAME = 'Eric Idle'

    contents = {
        'greeting': HOLA,
        'name': NAME
    }
    container(contents)

    @inject
    def greet(greeting, name):
        return '{} {}'.format(greeting, name)

    assert (HOLA + ' ' + OTHER_NAME) == greet(name=OTHER_NAME)

def test_replaces_kwonly_args():
    HOLA = 'hola'
    NAME = 'John Cleese'

    contents = {
        'greeting': HOLA,
        'name': NAME
    }
    container(contents)

    @inject
    def greet(greeting, *, name=None):
        return '{} {}'.format(greeting, name)

    assert (HOLA + ' ' + NAME) == greet()

def test_replaces_named_kwargs_args():
    HOLA = 'hola'
    NAME = 'John Cleese'

    contents = {
        'fullgreeting': {
            'greeting': HOLA,
            'name': NAME
        }
    }
    container(contents)

    @inject
    def greet(**fullgreeting):
        return '{} {}'.format(fullgreeting['greeting'], fullgreeting['name'])

    assert (HOLA + ' ' + NAME) == greet()


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

def test_all_types_of_params():

    contents = {
        'posonly': 1,
        'pos': 2,
        'fulltuple': (1, 2),
        'kwonly': 'hola',
        'fulldict': {
            'greeting': 'hola',
        }
    }
    container(contents)

    @inject
    def difficult(posonly, /, pos, *fulltuple, kwonly=None, **fulldict):
        return {
            'posonly': posonly,
            'pos': pos,
            'fulltuple': fulltuple,
            'kwonly': kwonly,
            'fulldict': fulldict
        }
    result = difficult()

    assert contents == result

def test_all_types_of_params_with_extras():

    contents = {
        'posonly': 1,
        'pos': 2,
        'fulltuple': (1, 2),
        'kwonly': 'hola',
        'fulldict': {
            'greeting': 'hola',
        },
        'name': 'Michael Palin'
    }
    container(contents)

    @inject
    def difficult(posonly, /, pos, *fulltuple, kwonly=None, **fulldict):
        return {
            'posonly': posonly,
            'pos': pos,
            'fulltuple': fulltuple,
            'kwonly': kwonly,
            'fulldict': fulldict,
            'name': fulldict['name']
        }
    result = difficult(3, 4, 5, 6, kwonly='adeu', name=None)
    expected = {
        'posonly': 3,
        'pos': 4,
        'fulltuple': (5, 6, 1, 2),
        'kwonly': 'adeu',
        'fulldict': {
            'greeting': 'hola',
            'name': 'Michael Palin'
        },
        'name': 'Michael Palin'
    }

    assert expected == result
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
