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

from bpy.types import NodeTree
from .registration import register_class


@register_class
class ProceduralTextureNodeTree(NodeTree):
    bl_idname = 'ProceduralTextureNodeTree'
    bl_label = 'Procedural Texture Editor'
    bl_icon = 'NODETREE'

    def update(self):
        from .nodes.output_node import OutputNode
        for node in self.nodes:
            if isinstance(node, OutputNode):
                node.backUpdate()

    def interface_update(self, context):  # when does this get called?
        pass
