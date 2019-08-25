# Copyright (C) 2019 Adrian Guerra
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see https://www.gnu.org/licenses/.

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
