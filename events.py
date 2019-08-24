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
