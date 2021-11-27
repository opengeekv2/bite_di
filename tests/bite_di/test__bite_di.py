from bite_di import container, inject

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
    OTHER_NAME = 'John Cleese'
    contents = {
        'greeting': HOLA,
        'name': NAME
    }
    container(contents)

    @inject
    def greet(greeting: str = HELLO, name: str = OTHER_NAME):
        return '{} {}'.format(greeting, name)

    assert (HOLA + ' ' + NAME) == greet()





