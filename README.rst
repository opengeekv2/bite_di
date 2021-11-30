Bite Dependency Injection
=========================

.. |cibadge| image:: https://github.com/opengeekv2/bite_di/actions/workflows/ci.yml/badge.svg
    :alt: ci badge
    :target: https://github.com/opengeekv2/bite_di/actions/workflows/ci.yml?query=branch%3Amain++
.. |testcoverage| image:: https://codecov.io/gh/opengeekv2/bite_di/branch/main/graph/badge.svg?flag=test-coverage
    :alt: Test coverage badge
    :target: https://codecov.io/gh/opengeekv2/bite_di
.. |mypybadge| image:: https://img.shields.io/static/v1?label=mypy&message=checked&color=blue&logo=data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMTQiIGhlaWdodD0iMTQiIHhtbG5zPSJodHRwOi8vd3d3LnczLm9yZy8yMDAwL3N2ZyIgdmVyc2lvbj0iMS4xIj4KIDxtZXRhZGF0YSBpZD0ibWV0YWRhdGE3Ij5pbWFnZS9zdmcreG1sPC9tZXRhZGF0YT4KCiA8Zz4KICA8dGl0bGU+TGF5ZXIgMTwvdGl0bGU+CiAgPHBhdGggc3Ryb2tlPSJudWxsIiBmaWxsLXJ1bGU9Im5vbnplcm8iIGZpbGw9IiMyYTZkYjIiIGQ9Im03LjAwOTU4LDBjLTMuNTIwODUsMCAtMy4zMDA5OSwxLjUzNjY3IC0zLjMwMDk5LDEuNTM2NjdsMC4wMDM5MiwxLjU5MTk4bDMuMzU5ODYsMGwwLDAuNDc3OTlsLTQuNjk0MzksMGMwLDAgLTIuMjUyOTksLTAuMjU3MTUgLTIuMjUyOTksMy4zMTgyN2MwLDMuNTc1NDIgMS45NjY0NiwzLjQ0ODYzIDEuOTY2NDYsMy40NDg2M2wxLjE3MzYsMGwwLC0xLjY1OTEzYzAsMCAtMC4wNjMyNiwtMS45NzkxMSAxLjkzNTA2LC0xLjk3OTExYzEuOTk4MzIsMCAzLjMzMjM5LDAgMy4zMzIzOSwwYzAsMCAxLjg3MjI2LDAuMDMwNDYgMS44NzIyNiwtMS44MjExYzAsLTEuODUxNTYgMCwtMy4wNjE1IDAsLTMuMDYxNWMwLDAgMC4yODQyNiwtMS44NTI3IC0zLjM5NTE5LC0xLjg1MjdsMCwwbDAuMDAwMDEsMHptLTEuODUyNjMsMS4wNzA1NGMwLjMzNDI4LDAgMC42MDQ0NiwwLjI3MTkyIDAuNjA0NDYsMC42MDgzNWMwLDAuMzM2NDMgLTAuMjcwMTgsMC42MDgzNSAtMC42MDQ0NiwwLjYwODM1Yy0wLjMzNDI4LDAgLTAuNjA0NDYsLTAuMjcxOTIgLTAuNjA0NDYsLTAuNjA4MzVjMCwtMC4zMzY0MyAwLjI3MDE4LC0wLjYwODM1IDAuNjA0NDYsLTAuNjA4MzV6IiBpZD0icGF0aDg2MTUiLz4KICA8cGF0aCBzdHJva2U9Im51bGwiIGZpbGwtcnVsZT0ibm9uemVybyIgZmlsbD0iI2RmZGZkZiIgaWQ9InBhdGg4NjIwIiBkPSJtNy4xMDk1NywxMy44ODU2NmMzLjUyMDg1LDAgMy4zMDA5OSwtMS41MzY2NyAzLjMwMDk5LC0xLjUzNjY3bC0wLjAwMzkyLC0xLjU5MTk4bC0zLjM1OTg2LDBsMCwtMC40Nzc5OWw0LjY5NDM5LDBjMCwwIDIuMjUyOTksMC4yNTcxNSAyLjI1Mjk5LC0zLjMxODI3YzAsLTMuNTc1NDIgLTEuOTY2NDYsLTMuNDQ4NjMgLTEuOTY2NDYsLTMuNDQ4NjNsLTEuMTczNiwwbDAsMS42NTkxM2MwLDAgMC4wNjMyNiwxLjk3OTExIC0xLjkzNTA2LDEuOTc5MTFjLTEuOTk4MzIsMCAtMy4zMzIzOSwwIC0zLjMzMjM5LDBjMCwwIC0xLjg3MjI2LC0wLjAzMDQ2IC0xLjg3MjI2LDEuODIxMWMwLDEuODUxNTUgMCwzLjA2MTQ5IDAsMy4wNjE0OWMwLDAgLTAuMjg0MjYsMS44NTI3IDMuMzk1MTksMS44NTI3bDAsMGwtMC4wMDAwMSwwLjAwMDAxem0xLjg1MjYzLC0xLjA3MDU0Yy0wLjMzNDI4LDAgLTAuNjA0NDYsLTAuMjcxOTIgLTAuNjA0NDYsLTAuNjA4MzVjMCwtMC4zMzY0MyAwLjI3MDE4LC0wLjYwODM1IDAuNjA0NDYsLTAuNjA4MzVjMC4zMzQyOCwwIDAuNjA0NDYsMC4yNzE5MiAwLjYwNDQ2LDAuNjA4MzVjMCwwLjMzNjQzIC0wLjI3MDE4LDAuNjA4MzUgLTAuNjA0NDYsMC42MDgzNXoiLz4KIDwvZz4KPC9zdmc+
    :alt: Mypy badge
    :target: http://mypy-lang.org/
.. |typesbadge| image:: https://codecov.io/gh/opengeekv2/bite_di/branch/main/graph/badge.svg?flag=type-coverage
    :alt: Types coverage badge
    :target: https://codecov.io/gh/opengeekv2/bite_di

|cibadge| |testcoverage| |mypybadge| |typesbadge|



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















