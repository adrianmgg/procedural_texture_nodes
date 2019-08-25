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

import pkgutil
from bpy.utils import register_class, unregister_class
from . import registration
import nodeitems_utils

bl_info = {
    "name": "Procedural Texture Nodes",
    "author": "Adrian Guerra",
    "description": "",
    "blender": (2, 80, 0),
    "version": (0, 0, 1),
    "location": "",
    "warning": "",
    "category": "Node"
}

print('''\
############################
# Procedural Texture Nodes #
############################''')

# TODO move this into register function? (first run only)
print('importing stuff')
__path__ = pkgutil.extend_path(__path__, __name__)
for module_loader, name, ispkg in pkgutil.walk_packages(path=__path__, prefix=f'{__name__}.'):
    print(f'    importing {name}')
    __import__(name)


def register():
    for cls in registration.classes_to_register:
        register_class(cls)
        print(f'registered {cls}')
    nodeitems_utils.register_node_categories('PROCEDURALTEXTURENODES', registration.node_categories_to_register)


def unregister():
    nodeitems_utils.unregister_node_categories('PROCEDURALTEXTURENODES')
    for cls in registration.classes_to_register:
        unregister_class(cls)
        print(f'unregistered {cls}')
