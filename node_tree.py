from bpy.types import NodeTree
from .registration import register_class


@register_class
class ProceduralTextureNodeTree(NodeTree):
    '''Description'''
    bl_idname = 'ProceduralTextureNodeTree'
    bl_label = 'Procedural Texture Editor'
    bl_icon = 'NODETREE'

    def update(self):
        print(f'{self}.update()')

    def interface_update(self, context):  # TODO when does this get called
        print(f'{self}.interface_update({context})')
