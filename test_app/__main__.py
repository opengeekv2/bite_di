from ._services import *
from bite_di import inject

@inject
def hola(a=None):
    pass

