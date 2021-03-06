from bite_di import container, inject, Contents


def test_all_types_of_params():
    expected = {
        'posonly': 1,
        'pos': 2,
        'fulltuple': (1, 2),
        'kwonly': 'hola',
        'fulldict': {
            'greeting': 'hola',
        }
    }
    contents = Contents()
    contents.from_var_dict(expected)
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

    assert expected == result


def test_all_types_of_params_with_extras():
    contents = Contents()
    contents.from_var_dict({
        'posonly': 1,
        'pos': 2,
        'fulltuple': (1, 2),
        'kwonly': 'hola',
        'fulldict': {
            'greeting': 'hola',
        },
        'name': 'Michael Palin'
    })
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
