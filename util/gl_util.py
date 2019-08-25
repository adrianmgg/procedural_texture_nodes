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

from typing import Union
import gpu
from mathutils import Matrix
import gpu_extras


# TODO give this a better name
class OffscreenRendering:
    def __init__(self, width: int, height: int, samples: int = 0):
        self.width = width
        self.height = height
        self.samples = samples
        self._offscreen: Union[gpu.types.GPUOffScreen, None] = None

    def __enter__(self):
        self._offscreen = gpu.types.GPUOffScreen(self.width, self.height, self.samples)
        self._offscreen.bind()
        gpu.matrix.load_matrix(Matrix.Identity(4))
        gpu.matrix.load_projection_matrix(Matrix.Identity(4))
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._offscreen.unbind()
        self._offscreen.free()
