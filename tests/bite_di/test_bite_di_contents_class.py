from bite_di import container


def test_contents_are_set_from_var_dict() -> None:
    vardict = {
        'key': 'value'
    }
    container(vardict)
    assert 'value' == container.get('key')


def test_contents_are_add_key_value() -> None:
    container.add_var('key', 'value')
    assert 'value' == container.get('key')


def test_contents_are_add_factory() -> None:
    container.add_factory('key', lambda: 'value')
    assert 'value' == container.get('key')
