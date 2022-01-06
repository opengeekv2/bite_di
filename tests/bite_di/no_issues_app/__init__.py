from bite_di import inject, container


container({
    'a': 1   
})

@inject
def hola(a: str = None):
    pass

hola()