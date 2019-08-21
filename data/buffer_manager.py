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


def free_instance(key: int) -> NoReturn:
    if key in _buffer_instances:
        bgl.glDeleteTextures(1, _buffer_instances.pop(key))
        _buffer_types.pop(key)


def replace_instance(key: int, buffer_type: int, dimensions: Union[int, List[int]], template=None) -> NoReturn:
    free_instance(key)
    _create_buffer(key=key, buffer_type=buffer_type, dimensions=dimensions, template=template)


def get_buffer_type(key: int) -> int:
    return _buffer_types.get(key)
