import bpy
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from .base_types.node import ProceduralTextureNode


# TODO "there are no safety checks to avoid infinite recursion." - add that check
def nodePropertyChanged(node: 'ProceduralTextureNode', context: bpy.types.Context):
    node.updateNode()
