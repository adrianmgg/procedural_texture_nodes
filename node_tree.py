from bpy.types import NodeTree
from .registration import register_class

@register_class
class ProceduralTextureNodeTree(NodeTree):
    '''Description'''
    bl_idname = 'ProceduralTextureNodeTree'
    bl_label = 'Procedural Texture Editor'
    bl_icon = 'NODETREE'