from typing import Union, Optional, NoReturn, List, Dict

import bgl
from bgl import Buffer

_buffer_instances: Dict[int, bgl.Buffer] = {}
_count: int = 0


def _create_buffer(buffer_type: int, dimensions: Union[int, List[int]], template=None) -> Buffer:
    if template is None:
        return Buffer(buffer_type, dimensions)
    else:
        return Buffer(buffer_type, dimensions, template)


# https://docs.blender.org/api/current/bgl.html#bgl.Buffer
def new_instance(buffer_type: int, dimensions: Union[int, List[int]], template=None) -> int:
    global _count
    _count += 1
    _buffer_instances[_count] = _create_buffer(buffer_type=buffer_type, dimensions=dimensions, template=template)
    return _count


def get_instance(key: int) -> Optional[bgl.Buffer]:
    if key in _buffer_instances:
        return _buffer_instances[key]
    return None


def free_instance(key: int) -> NoReturn:
    if key in _buffer_instances:
        _buffer_instances.pop(key)  # FIXME BUFFER ISN'T DELETED


def replace_instance(key: int, buffer_type: int, dimensions: Union[int, List[int]], template=None)\
        -> NoReturn:
    free_instance(key)
    _buffer_instances[key] = _create_buffer(buffer_type=buffer_type, dimensions=dimensions, template=template)
