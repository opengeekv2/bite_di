Bite Dependency Injection
=========================

.. image:: https://github.com/opengeekv2/bite_di/actions/workflows/ci.yml/badge.svg

.. image:: https://codecov.io/gh/opengeekv2/bite_di/branch/main/graph/badge.svg?token=8X8XL7D1D6
    :alt: Codecov badge
    :target: https://codecov.io/gh/opengeekv2/bite_di

Bitesized Dependency Injection library for Python.

Provides a easy and low footprint solution to inject dependecies to your Python functions and classes.

Why?
----
Mainly out of curiosity of how something like that could be designed and implemented with Python and mainly after visiting this `StackOverflow thread <https://stackoverflow.com/questions/2461702/why-is-ioc-di-not-common-in-python>`_.

How?
----
The design and implementation of the library tries to borrow implementation patterns class-centric languages.
It tries to avoid the use of use of classes for functionality that requires no state. If something can be just a function call it is.

It also leverages Python functional scope to provide private containers so you can use DI in your library without being at risk of someone messing up with your services afterwards.

Key features:

- [x] Global container
- [x] Private containers
- [x] Full Python setup (no config files in YAML or XML) 
- [x] @inject decorator
- [x] inject name-matching positional agruments
- [x] inject name-matching keyword only arguments 
- [x] inject name-matching keyword arguments passed as None
- [x] Basic container dump 

Using the public container
-----------------------------

Add services or replace services in the public container:

It is recommended that you do this in a _services.py module in your package.

.. code-block:: python
    
    from bite_di import container
    from .infrastructure import implementation #this is a function in another module

    def _feed_container():
        contents = {
            'interface': implementation
        }
        container(contents)

    _feed_container()

Using the `IIFE idiom <https://en.wikipedia.org/wiki/Immediately_invoked_function_expression>`_ is recomended so the contenst dict can't be checked or modified by outsiders. The only way to override a service should be to call container(contents) again with a new value associated to the same key.
This idiom will be crucial for implementing private containers. Also the only way to get a service injected is using the inject decorator.

Then in your __main__.py your main script or the entrypoint you are using you must import _services.py.

.. code-block:: python
    
    import _services #your linter may report unused import or
    from ._services import * #you are im

    #your app entrypoint

Then in any place of your app you can use inject to awtowire parameters that match a key in the container.

.. code-block:: python
    
    from bite_di import inject

    @inject
    def client(interface):
        return interface()

    print(client()) # will print implementation return value

As the container memory is in the library everytime you call bite_di.container new key-values are added or overriden.
There might be a situation where you may want to see what is in you container. Any call to container returns a tuple with the inject decorator for that container and a dump function that can be handy to inspect the contents in console.

.. code-block:: python
    
    from bite_di import container

    inject, dump = container() # Empty calls to container are valid

    dump() # outputs {'interface': <function implementation at 0x7f976c946440>}

As the basis of the container is a polymorphic dictionary you can put anything to it. There's only one exception that is None. None values will not be injected and it is advised that you use default parameters as None in your decorated function for that.















