import bpy
from bpy.types import Node

from ..node_tree import ProceduralTextureNodeTree

from typing import TYPE_CHECKING, List

if TYPE_CHECKING:
    from ..base_types.socket import ProceduralTextureNodeSocket


class ProceduralTextureNode(Node):
    outputs: List['ProceduralTextureNodeSocket']
    inputs: List['ProceduralTextureNodeSocket']

    def init_post(self):
        self.updateNode()

    @classmethod
    def poll(cls, tree: 'bpy.types.NodeTree'):
        return tree.bl_idname == ProceduralTextureNodeTree.bl_idname

    def update(self):
        pass

    def socket_value_update(self, context: 'bpy.types.Context'):  # does this do anything
        pass

    def draw_buttons(self, context: 'bpy.types.Context', layout: 'bpy.types.UILayout'):
        pass

    def updateNode(self):
        print(f'updating node {self.name}')
        self.recalculateOutputs()
        for output in self.outputs:
            output.update()

    def recalculateOutputs(self):
        pass
