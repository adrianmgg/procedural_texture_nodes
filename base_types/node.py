from bpy.types import Node
from ..node_tree import ProceduralTextureNodeTree


class ProceduralTextureNode(Node):
    @classmethod
    def poll(cls, tree):
        print(f'polling {tree.bl_idname == ProceduralTextureNodeTree.bl_idname}')
        return tree.bl_idname == ProceduralTextureNodeTree.bl_idname
