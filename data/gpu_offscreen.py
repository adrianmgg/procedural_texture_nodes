import gpu
import typing

_gpu_offscreen_instances: typing.Dict[int, gpu.types.GPUOffScreen] = {}
_count: int = -1


def new_instance(width: int, height: int, samples: int = 0) -> int:
    global _count
    _count += 1
    _gpu_offscreen_instances[_count] = gpu.types.GPUOffScreen(width, height, samples)
    return _count


def get_instance(key: int) -> typing.Optional[gpu.types.GPUOffScreen]:
    if key in _gpu_offscreen_instances:
        return _gpu_offscreen_instances[key]
    return None


def free_instance(key: int) -> typing.NoReturn:
    if key in _gpu_offscreen_instances:
        _gpu_offscreen_instances.pop(key).free()


def replace_instance(key: int, width: int, height: int, samples: int = 0) -> typing.NoReturn:
    free_instance(key)
    _gpu_offscreen_instances[key] = gpu.types.GPUOffScreen(width, height, samples)
