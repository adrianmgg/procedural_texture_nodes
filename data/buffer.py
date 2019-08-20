import bgl
from bgl import Buffer
import typing
from enum import Enum

_buffer_instances: typing.Dict[int, bgl.Buffer] = {}
_count: int = -1


# https://docs.blender.org/api/current/bgl.html#bgl.Buffer
def new_instance(buffer_type: int, dimensions: typing.Union[int, typing.List[int]], template=None) -> int:
    print(f'''\
new_instance(
    buffer_type={buffer_type},
    dimensions={dimensions},
    template={template}
)''')
    global _count
    _count += 1
    if template is None:
        _buffer_instances[_count] = Buffer(buffer_type, dimensions)
    else:
        _buffer_instances[_count] = Buffer(buffer_type, dimensions, template)
    return _count


def get_instance(key: int) -> typing.Optional[bgl.Buffer]:
    if key in _buffer_instances:
        return _buffer_instances[key]
    return None


def free_instance(key: int) -> typing.NoReturn:
    if key in _buffer_instances:
        _buffer_instances.pop(key)  # TODO how to free/delete a buffer?


def replace_instance(key: int, buffer_type: int, dimensions: typing.Union[int, typing.List[int]], template=None)\
        -> typing.NoReturn:
    free_instance(key)
    if template is None:
        _buffer_instances[_count] = Buffer(buffer_type, dimensions)
    else:
        _buffer_instances[_count] = Buffer(buffer_type, dimensions, template)
