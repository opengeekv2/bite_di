from bite_di import container, Container


def test_container_not_recreated_after_import() -> None:
    from bite_di import container as c1
    assert c1 == container


def test_container_not_recreated_after_create_container() -> None:
    from bite_di import container as c1, Container
    assert c1 != Container()
    assert c1 == container


def test_container_dump(capsys):
    container = Container()
    contents = {}
    contents['greeting'] = 'hola'
    container(contents)
    container.dump()
    captured = capsys.readouterr()
    assert captured.out == "{'greeting': 'hola'}\n"
