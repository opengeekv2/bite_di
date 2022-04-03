from bite_di import container


def test_contents_are_set_from_var_dict() -> None:
    container(lambda add_dependency: add_dependency('key', lambda: 'value' ))
    assert 'value' == container.get('key')

def test_contents_are_add_factory() -> None:
    container.add_factory('key', lambda: 'value')
    assert 'value' == container.get('key')
