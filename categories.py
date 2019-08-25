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

from nodeitems_utils import NodeCategory
from . import registration
from .node_tree import ProceduralTextureNodeTree


class ProceduralTextureNodeCategory(NodeCategory):
    @classmethod
    def poll(cls, context):
        return context.space_data.tree_type == ProceduralTextureNodeTree.bl_idname

    def __init__(self, identifier, name, description=''):
        self._items = []
        super().__init__(identifier, name, description, self._items)
        registration.node_categories_to_register.append(self)

    def append(self, node):
        self._items.append(node)


# use an enum for these?
test_nodes = ProceduralTextureNodeCategory(
    identifier='TEST',
    name='Test Category'
)

noise_nodes = ProceduralTextureNodeCategory(
    identifier='NOISE',
    name='Noise'
)

effects = ProceduralTextureNodeCategory(
    identifier='EFFECTS',
    name='Effects'
)

io_nodes = ProceduralTextureNodeCategory(
    identifier='IO',
    name='Input/Output'
)
