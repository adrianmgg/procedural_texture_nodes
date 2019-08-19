import bpy
import gpu
import gpu_extras
from ..base_types.node import ProceduralTextureNode
from ..registration import register_node
from .. import categories
from ..sockets.image_socket import ImageSocket


@register_node(category=categories.test_nodes)
class TestNode(ProceduralTextureNode):
    '''description'''
    bl_idname = 'ProceduralTexture_Test'
    bl_label = 'Test Node'

    def init(self, context):
        self.image_output = self.outputs.new(ImageSocket.bl_idname, 'Image')
        self.image_data = gpu.types.GPUOffScreen(512, 512)

    def free(self):
        self.image_data.free()
