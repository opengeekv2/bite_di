from bite_di import container, Contents
from bite_di.di import create_container


def test_container_not_recreated_after_import() -> None:
    from bite_di import container as c1
    assert c1 == container


def test_container_not_recreated_after_create_container() -> None:
    from bite_di import container as c1, create_container
    assert c1 != create_container()
    assert c1 == container


def test_container_dump(capsys):
    container = create_container()
    contents = Contents()
    contents['greeting'] = lambda: 'hola'
    container(contents)
    container.dump()
    captured = capsys.readouterr()
    assert captured.out == "{'greeting': 'hola'}\n"
