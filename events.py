import bpy
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from .base_types.node import ProceduralTextureNode


def node_property_update(node: 'ProceduralTextureNode', context: bpy.types.Context):
    node.updateNode()
