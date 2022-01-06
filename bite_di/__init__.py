from .di import Container

if 'container' not in locals().keys():
    container = Container()
inject = container()
