import bgl
import bpy
import gpu
import gpu_extras
from gpu_extras.presets import draw_circle_2d
from ..base_types.node import ProceduralTextureNode
from ..registration import register_node
from .. import categories
from ..sockets.image_socket import ImageSocket
from ..data import buffer as buffer_manager
from mathutils import Matrix


def dimensions_changed(node: 'TestNode', context: bpy.types.Context):
    buffer_manager.replace_instance(
        key=node.buffer_id,
        buffer_type=bgl.GL_BYTE,
        dimensions=4 * node.image_width * node.image_height
    )
    node.buffer_needs_update = True
    node.updateNode()


@register_node(category=categories.test_nodes)
class TestNode(ProceduralTextureNode):
    '''description'''
    bl_idname = 'ProceduralTexture_Test'
    bl_label = 'Test Node'

    image_width: bpy.props.IntProperty(default=1024, min=1, update=dimensions_changed)
    image_height: bpy.props.IntProperty(default=1024, min=1, update=dimensions_changed)

    buffer_id: bpy.props.IntProperty(default=-1)
    buffer_needs_update: bpy.props.BoolProperty(default=True)

    def init(self, context):
        self.buffer_id = buffer_manager.new_instance(
            buffer_type=bgl.GL_BYTE,
            dimensions=4 * self.image_width * self.image_height
        )
        self.outputs.new(ImageSocket.bl_idname, name='Output')

    def draw_buttons(self, context, layout):
        layout.prop(self, 'image_width', text='Width')
        layout.prop(self, 'image_height', text='Height')

    def updateNode(self):
        buffer_output: ImageSocket = self.outputs.get('Output')
        buffer_output.set_buffer_id(self.buffer_id)
        buffer_output.width = self.image_width
        buffer_output.height = self.image_height
        if self.buffer_needs_update and self.buffer_id is not -1:
            offscreen = gpu.types.GPUOffScreen(self.image_width, self.image_height)
            with offscreen.bind():
                gpu.matrix.load_matrix(Matrix.Identity(4))
                gpu.matrix.load_projection_matrix(Matrix.Identity(4))
                for x in range(-8, 8 + 1):
                    draw_circle_2d(
                        (x / 8, 0),  # position
                        (1, 1, 1, 1),  # color
                        .25,  # radius
                        32  # segments
                    )
                self.buffer_needs_update = False

                buffer = buffer_manager.get_instance(self.buffer_id)
                bgl.glReadBuffer(bgl.GL_BACK)
                bgl.glReadPixels(0, 0, self.image_width, self.image_height, bgl.GL_RGBA, bgl.GL_UNSIGNED_BYTE, buffer)

    def free(self):
        buffer_manager.free_instance(self.buffer_id)
