from bite_di import Contents


def test_contents_are_set_from_var_dict() -> None:
    contents = Contents()
    vardict = {
        'key': 'value'
    }
    contents.from_var_dict(vardict)
    assert 'value' == contents['key']()


def test_contents_are_add_key_value() -> None:
    contents = Contents()
    contents.add_var('key', 'value')
    assert 'value' == contents['key']()


def test_contents_are_add_factory() -> None:
    contents = Contents()
    contents.add_factory('key', lambda: 'value')
    assert 'value' == contents['key']()
