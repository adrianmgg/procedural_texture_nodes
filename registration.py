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

import nodeitems_utils
from typing import TYPE_CHECKING, Type

if TYPE_CHECKING:
    from .categories import ProceduralTextureNodeCategory
    from .base_types.node import ProceduralTextureNode

classes_to_register = set()
node_categories_to_register = []


def _fix_property_inheritance(cls):
    # give properties of superclasses to class
    # TODO make this less ugly
    annotations = {}
    for a in reversed(cls.mro()):
        if '__annotations__' in dir(a):
            for k, v in a.__annotations__.items():
                # check if annotation is a property annotation
                if isinstance(v, tuple) and len(v) == 2 and v[0].__module__ == 'bpy.props':
                    annotations[k] = v
    if len(annotations) > 0:
        cls.__annotations__ = annotations


def register_class(cls):
    _fix_property_inheritance(cls)
    classes_to_register.add(cls)
    return cls


def register_node(category: 'ProceduralTextureNodeCategory'):
    def decorator(cls: 'Type[ProceduralTextureNode]'):
        _fix_property_inheritance(cls)
        category.append(nodeitems_utils.NodeItem(cls.bl_idname))
        classes_to_register.add(cls)
        return cls

    return decorator
