import bpy
from bpy.types import Node


class ProceduralTextureNode(Node):
    initialization_completed: bpy.props.BoolProperty(default=False)

    is_dirty: bpy.props.BoolProperty(default=True)

    def init(self, context):
        self.initialization_completed = False
        self.init_node(context)
        self.initialization_completed = True

    def init_node(self, context: 'bpy.types.Context'):
        pass

    @classmethod
    def poll(cls, tree: 'bpy.types.NodeTree'):
        from ..node_tree import ProceduralTextureNodeTree
        return tree.bl_idname == ProceduralTextureNodeTree.bl_idname

    def update(self):
        self.is_dirty = True

    def socket_value_update(self, context: 'bpy.types.Context'):  # does this do anything?
        pass

    def draw_buttons(self, context: 'bpy.types.Context', layout: 'bpy.types.UILayout'):
        pass

    def updateNode(self):
        self.is_dirty = True
        for output in self.outputs:
            output.update()

    def recalculateOutputs(self):
        self.is_dirty = False

    def backUpdate(self):
        for ipt in self.inputs:
            if ipt.is_linked:
                for link in ipt.links:
                    if link.from_node.is_dirty:
                        link.from_node.backUpdate()
        self.recalculateOutputs()
