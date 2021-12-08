from typing import Optional, Callable, Awaitable
from bite_di import create_container, Contents
import asyncio


def test_injects_to_async_function():
    container = create_container()
    contents = Contents()

    contents.from_var_dict({
        'a': 'hola'
    })

    inject, dump = container(contents)

    @inject
    async def hola(a: Optional[str] = None):
        if a is not None:
            return a

    result = asyncio.run(hola())
    assert 'hola' == result


def test_injects_async_function_to_async_function():
    container = create_container()
    contents = Contents()

    async def return_hola() -> str:
        return await asyncio.sleep(1, 'hola')

    contents.from_var_dict({
        'a': return_hola
    })

    inject, dump = container(contents)

    @inject
    async def hola(a: Callable[[], Awaitable[str]] = None):
        if a is not None:
            return await a()

    result = asyncio.run(hola())
    assert 'hola' == result
