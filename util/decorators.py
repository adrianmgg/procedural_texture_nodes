from functools import wraps
import typing
from typing import TYPE_CHECKING

import bpy

if TYPE_CHECKING:
    from ..base_types.socket import ProceduralTextureNodeSocket


def get_from_linked(function):
    @wraps(function)
    def wrapper(self: 'ProceduralTextureNodeSocket', *args, **kwargs):
        if not self.is_output and len(self.links) > 0:
            link = self.links[0]
            # TODO check what link.is_valid is
            if link.from_socket is not None and function.__name__ in dir(link.from_socket):
                return getattr(link.from_socket, function.__name__)(*args, **kwargs)
        return function(self, *args, **kwargs)
    return wrapper


def add_handler(handler):
    def decorator(function):
        handler.append(function)
        return function
    return decorator
