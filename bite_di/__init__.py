from .di import create_container, Contents  # noqa: F401

if 'container' not in locals().keys():
    container = create_container()
inject, dump = container()
