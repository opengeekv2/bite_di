from .di import create_container


if 'container' not in locals():
    container = create_container()
inject, dump = container()
