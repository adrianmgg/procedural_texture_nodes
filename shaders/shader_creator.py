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

import os

from typing import Optional, List

shaders_dir = os.path.dirname(os.path.realpath(__file__))


def load_shader_file(shader_path: str, shaders_already_imported: Optional[List[str]] = None, shader_file_type: str = 'frag') -> str:
    if shaders_already_imported is None:
        shaders_already_imported = []

    shader_file_contents = ''

    shader_file_path = os.path.join(shaders_dir, f'{shader_path}.{shader_file_type}')
    dependencies_file_path = os.path.join(shaders_dir, f'{shader_path}.dependencies')

    if not os.path.exists(shader_file_path):
        raise Exception(f'Shader file "{shader_path}.{shader_file_type}" not found')

    if os.path.exists(dependencies_file_path):
        with open(dependencies_file_path, 'r') as dependencies_file:
            for dependency in dependencies_file:
                dependency = dependency.rstrip()
                if dependency not in shaders_already_imported:
                    shader_file_contents += '\n'
                    shader_file_contents += load_shader_file(dependency, shaders_already_imported)

    with open(shader_file_path, 'r') as shader_file:
        shader_file_contents += '\n'
        shader_file_contents += shader_file.read()

    return shader_file_contents
