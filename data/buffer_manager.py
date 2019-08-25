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

from typing import Union, Optional, NoReturn, List, Dict

import bgl
from bgl import Buffer

_buffer_instances: Dict[int, bgl.Buffer] = {}
_buffer_types: Dict[int, int] = {}
_count: int = 0


def _create_buffer(key: int, buffer_type: int, dimensions: Union[int, List[int]], template=None) -> NoReturn:
    if template is None:
        _buffer_instances[key] = Buffer(buffer_type, dimensions)
    else:
        _buffer_instances[key] = Buffer(buffer_type, dimensions, template)
    _buffer_types[key] = buffer_type


def new_instance(buffer_type: int, dimensions: Union[int, List[int]], template=None) -> int:
    global _count
    _count += 1
    _create_buffer(key=_count, buffer_type=buffer_type, dimensions=dimensions, template=template)
    return _count


def get_instance(key: int) -> Optional[bgl.Buffer]:
    if key in _buffer_instances:
        return _buffer_instances[key]
    return None


def delete_instance(key: int) -> NoReturn:
    if key in _buffer_instances:
        _buffer_instances.pop(key)
        _buffer_types.pop(key)


def replace_instance(key: int, buffer_type: int, dimensions: Union[int, List[int]], template=None) -> NoReturn:
    delete_instance(key)
    _create_buffer(key=key, buffer_type=buffer_type, dimensions=dimensions, template=template)


def get_buffer_type(key: int) -> int:
    return _buffer_types.get(key)
