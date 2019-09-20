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

import gpu

from .shader_node import ShaderNode
from ..shaders.shader_creator import load_shader_file


class SimpleShaderNode(ShaderNode):
    _shader: 'gpu.types.GPUShader'

    def __init_subclass__(cls, fragment_shader: str = None) -> None:
        cls._shader = gpu.types.GPUShader(
            vertexcode=load_shader_file('shader_node', shader_file_type='vert'),
            fragcode=load_shader_file(fragment_shader, shader_file_type='frag')
        )

    @property
    def shader(self) -> 'gpu.types.GPUShader':
        return type(self)._shader
