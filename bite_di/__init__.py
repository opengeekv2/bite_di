from .di import create_container

if not 'container' in locals():
    container = create_container()
inject = container()