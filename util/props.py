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

from typing import Union, Tuple, List


# https://docs.blender.org/api/current/bpy.props.html#bpy.props.EnumProperty
EnumPropertyItems = List[Union[
    Tuple[str, str, str, Union[int, str], int],
    Tuple[str, str, str, int]
]]


def get_enum_prop_number(value: str, items: EnumPropertyItems):
    for item in items:
        if item[0] == value:
            return item[-1]
