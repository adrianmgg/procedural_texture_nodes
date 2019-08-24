import bpy
from bpy.types import Node

from ..node_tree import ProceduralTextureNodeTree


class ProceduralTextureNode(Node):

    initialization_completed: bpy.props.BoolProperty(default=False)

    def init(self, context):
        self.initialization_completed = False
        self.init_node(context)
        self.initialization_completed = True

    def init_node(self, context: 'bpy.types.Context'):
        pass

    @classmethod
    def poll(cls, tree: 'bpy.types.NodeTree'):
        return tree.bl_idname == ProceduralTextureNodeTree.bl_idname

    def update(self):
        if not self.initialization_completed:
            print('skipped early initialization')
            return
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
