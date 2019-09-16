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

from typing import List

shaders_dir = os.path.dirname(os.path.realpath(__file__))


def load_shader_file(shader_file_path: str) -> str:
    with open(os.path.join(shaders_dir, shader_file_path), 'r') as shader_file:
        return shader_file.read()


def load_shader_files(*shader_file_paths: str) -> str:
    return '\n'.join([load_shader_file(path) for path in shader_file_paths])
