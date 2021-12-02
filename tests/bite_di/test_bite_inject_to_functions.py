from __future__ import annotations
from typing import Dict
import pytest
from bite_di import container, inject, Contents


def test_replaces_function_args_for_container_string_keys_value() -> None:
    HOLA = 'hola'
    contents = Contents()
    contents.add_var('greeting', HOLA)
    container(contents)

    @inject
    def greet(greeting: str = None):
        return greeting

    assert HOLA == greet()


falsy_values_except_none = [
    [], (), {}, set(), '', b'', range(0), 0b0, 0x0, 00, 0, 0.0, 0j, False
]


@pytest.mark.parametrize('param', falsy_values_except_none)
def test_replaces_function_args_for_container_falsy_values_except_none(
        param) -> None:


    contents = Contents()
    contents.from_var_dict({
        'param': lambda: param
    })

    container(contents)

    @inject
    def greet(param=None):
        return param

    assert param == greet()


def test_does_not_replace_none_container_values() -> None:
    contents = Contents()
    contents.from_var_dict({
        'param': None
    })

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
    contents = Contents()
    contents.from_var_dict({
        'greeting': HOLA,
        'name': NAME
    })
    container(contents)

    @inject
    def greet(greeting: str, name: str = None):
        return '{} {}'.format(greeting, name)

    assert (HELLO + ' ' + NAME) == greet(HELLO)


def test_injects_varargs_by_key() -> None:
    HOLA = 'hola'
    NAME = 'John Cleese'
    contents = Contents()
    contents.from_var_dict({
        'fullgreeting': (HOLA, NAME)
    })
    container(contents)

    @inject
    def greet(*fullgreeting):
        greeting, name = fullgreeting
        return '{} {}'.format(greeting, name)

    assert (HOLA + ' ' + NAME) == greet()


def test_injects_varargs_by_key_but_are_merged_to_passed() -> None:
    HOLA = 'hola'
    NAME = 'John Cleese'
    contents = Contents()
    contents.from_var_dict({
        'fullgreeting': tuple([NAME])
    })
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
    contents = Contents()
    contents.from_var_dict({
        'greeting': HOLA,
        'name': NAME
    })
    container(contents)

    @inject
    def greet(greeting: str = HELLO, name: str = OTHER_NAME):
        return '{} {}'.format(greeting, name)

    assert (HOLA + ' ' + NAME) == greet()


def test_replaces_none_kwargs_with_ones_in_container() -> None:
    HOLA = 'hola'
    NAME = 'John Cleese'
    contents = Contents()
    contents.from_var_dict({
        'greeting': HOLA,
        'name': NAME
    })
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
    contents = Contents()
    contents.from_var_dict({
        'greeting': HOLA,
        'name': NAME
    })
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

    contents = Contents()
    contents.from_var_dict({
        'greeting': HOLA,
        'name': NAME
    })
    container(contents)

    @inject
    def greet(greeting, name):
        return '{} {}'.format(greeting, name)

    assert (HOLA + ' ' + OTHER_NAME) == greet(name=OTHER_NAME)


def test_replaces_kwonly_args():
    HOLA = 'hola'
    NAME = 'John Cleese'

    contents = Contents()
    contents.from_var_dict({
        'greeting': HOLA,
        'name': NAME
    })
    container(contents)

    @inject
    def greet(greeting, *, name=None):
        return '{} {}'.format(greeting, name)

    assert (HOLA + ' ' + NAME) == greet()


def test_replaces_named_kwargs_args():
    HOLA = 'hola'
    NAME = 'John Cleese'

    contents = Contents()
    contents.from_var_dict({
        'fullgreeting': {
            'greeting': HOLA,
            'name': NAME
        }
    })
    container(contents)

    @inject
    def greet(**fullgreeting):
        return '{} {}'.format(fullgreeting['greeting'], fullgreeting['name'])

    assert (HOLA + ' ' + NAME) == greet()


@pytest.mark.parametrize('param', falsy_values_except_none)
def test_replaces_function_kwargs_for_container_falsy_values_except_none(
        param) -> None:

    contents = Contents()
    contents.from_var_dict({
        'key': param
    })

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
    contents = Contents()
    contents.from_var_dict({
        'greeting': HOLA,
        'name': NAME,
    })
    container(contents)

    @inject
    def greet(greeting, name, **kwargs):
        other_greeting = kwargs['other_greeting']
        other_name = kwargs['other_name']
        return '{} {} {} {}'.format(greeting, name, other_greeting, other_name)

    assert (HOLA + ' ' + NAME + ' ' + HELLO + ' ' + OTHER_NAME
            == greet(HOLA, NAME, other_greeting=HELLO, other_name=OTHER_NAME))
