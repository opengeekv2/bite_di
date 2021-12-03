from .di import create_container, Contents


if 'container' not in locals().keys():
    container = create_container()
inject, dump = container()
