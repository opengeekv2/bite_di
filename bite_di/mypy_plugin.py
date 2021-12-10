from typing import Callable, Dict, Type
from typing import Optional,  Optional, Callable, Type, Any
from mypy.types import Instance
from mypy.plugin import FunctionContext, Plugin
from bite_di import container


class BiteDIPlugin(Plugin):
    def get_function_hook(self, fullname: str) -> Optional[Callable[[FunctionContext], Type]]:  # type: ignore
        def cb(fc: FunctionContext) -> Type:
            print([f.__qualname__ for f in container.decorated])
            if fullname in [f.__qualname__ for f in container.decorated]:
                print(fullname)
            return fc.default_return_type  # type: ignore
        
        return cb


def plugin(version: str):
    # ignore version argument if the plugin works with all mypy versions.
    return BiteDIPlugin
