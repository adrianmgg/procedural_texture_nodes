import bpy
from bpy.types import Node
from ..node_tree import ProceduralTextureNodeTree
from .. import events


# TODO give this a name that makes more sense - this is the base class for nodes in this plugin, not *just* procedural texture nodes in this plugin
class ProceduralTextureNode(Node):
    @classmethod
    def poll(cls, tree):
        return tree.bl_idname == ProceduralTextureNodeTree.bl_idname

    def update(self):
        print(f'{self}.update()')
        self.updateNode()

    def socket_value_update(self, context):  # does this do anything
        print(f'{self}.socket_value_update({context})')

    def draw_buttons(self, context: bpy.types.Context, layout: bpy.types.UILayout):
        pass

    def updateNode(self):
        pass
