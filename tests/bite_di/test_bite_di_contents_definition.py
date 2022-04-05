from bite_di import Container

def container_fixture() -> Container:
    return Container()

def test_contents_are_set_from_var_dict() -> None:
    container = container_fixture()
    container(lambda add_dependency: add_dependency('key', lambda: 'value' ))
    assert 'value' == container.get('key')

def test_contents_are_add_factory() -> None:
    container = container_fixture()
    container.add_factory('key', lambda: 'value')
    assert 'value' == container.get('key')
