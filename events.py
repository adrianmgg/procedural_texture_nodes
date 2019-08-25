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

from typing import TYPE_CHECKING

import bpy
from bpy.app.handlers import persistent

from .util.decorators import add_handler

if TYPE_CHECKING:
    from .node_tree import ProceduralTextureNodeTree
    from .base_types.node import ProceduralTextureNode
    from .base_types.socket import ProceduralTextureNodeSocket


def node_property_update(node: 'ProceduralTextureNode', context: 'bpy.types.Context'):
    node.updateNode()


def socket_property_update(socket: 'ProceduralTextureNodeSocket', context: 'bpy.types.Context'):
    socket.update()


@add_handler(bpy.app.handlers.load_post)
@persistent
def clear_node_buffers(_):
    for node_tree in bpy.data.node_groups:
        if node_tree.bl_idname == 'ProceduralTextureNodeTree':
            node_tree: 'ProceduralTextureNodeTree'
            for node in node_tree.nodes:
                node: 'ProceduralTextureNode'
                node.load()
            node_tree.update()
