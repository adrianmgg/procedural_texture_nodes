import bpy
from bpy.types import Node

from ..node_tree import ProceduralTextureNodeTree


class ProceduralTextureNode(Node):
    def init_post(self):
        self.updateNode()

    @classmethod
    def poll(cls, tree: 'bpy.types.NodeTree'):
        return tree.bl_idname == ProceduralTextureNodeTree.bl_idname

    def update(self):
        print(f'{self.name}.update()')
        self.updateNode()

    def socket_value_update(self, context: 'bpy.types.Context'):  # does this do anything
        pass

    def draw_buttons(self, context: 'bpy.types.Context', layout: 'bpy.types.UILayout'):
        pass

    def updateNode(self):
        self.recalculateOutputs()
        for output in self.outputs:
            output.update()

    def recalculateOutputs(self):
        pass
