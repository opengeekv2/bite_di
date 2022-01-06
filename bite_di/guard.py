from sys import argv
from inspect import signature, Parameter
from bite_di import container
import typeguard
import importlib

from bite_di.di import Container

class Result:
    def __init__(self):
        self.success = True
        self.messages = []

def _check_function(result, fun):
    sig = signature(fun)
    result.messages.append('def ' + fun.__qualname__ + str(sig))
    
    for param in signature(fun).parameters.values():
        if param.annotation is not Parameter.empty and container.get(param.name) is not None:
            try:
                typeguard.check_type(param.name, container.get(param.name), param.annotation)
            except TypeError as te:
                result.messages.append(str(te))
                result.success = False
    if result.success:
        result.messages.append('\nOk\n')
    return result

def run(pack, container: Container=container):
    result = Result()
    try:
        importlib.import_module(pack)
    except ModuleNotFoundError as mnfe:
        result.messages.append(str(mnfe))
        result.success = False

    for fun in container.decorated:
        result = _check_function(result, fun)

    return result

def command():

    if len(argv) < 2:
        print("Usage: bite_di <package_name>")
        exit(1)

    pack = argv[1]

    result = run(pack)

    for message in result.messages:
        print(message)

    if result.success is True:
        print('Success')
        exit()

    print('Error')
    exit(1)
