from bpy.types import NodeTree
from .registration import register_class


@register_class
class ProceduralTextureNodeTree(NodeTree):
    bl_idname = 'ProceduralTextureNodeTree'
    bl_label = 'Procedural Texture Editor'
    bl_icon = 'NODETREE'

    def update(self):
        from .nodes.output_node import OutputNode
        for node in self.nodes:
            if isinstance(node, OutputNode):
                node.backUpdate()

    def interface_update(self, context):  # when does this get called?
        pass
