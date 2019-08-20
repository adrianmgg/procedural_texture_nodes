import bpy
import gpu
import gpu_extras
from ..base_types.node import ProceduralTextureNode
from ..registration import register_node
from .. import categories
from ..sockets.image_socket import ImageSocket
from .. import events


@register_node(category=categories.test_nodes)
class TestNode(ProceduralTextureNode):
    '''description'''
    bl_idname = 'ProceduralTexture_Test'
    bl_label = 'Test Node'

    image_width: bpy.props.IntProperty(name='image_width', default=1024, min=1, update=events.nodePropertyChanged)
    image_height: bpy.props.IntProperty(name='image_height', default=1024, min=1, update=events.nodePropertyChanged)

    def init(self, context):
        self.image_output: ImageSocket = self.outputs.new(ImageSocket.bl_idname, 'Image Data')
        self.image_data = gpu.types.GPUOffScreen(512, 512)
        self.image_output.setValue(self.image_data)

    def draw_buttons(self, context, layout):
        layout.prop(self, 'image_width', text='Width')
        layout.prop(self, 'image_height', text='Height')

    def free(self):
        self.image_data.free()
