import bpy
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from .base_types.node import ProceduralTextureNode
    from .base_types.socket import ProceduralTextureNodeSocket


def node_property_update(node: 'ProceduralTextureNode', context: 'bpy.types.Context'):
    node.updateNode()


def socket_property_update(socket: 'ProceduralTextureNodeSocket', context: 'bpy.types.Context'):
    socket.update()
