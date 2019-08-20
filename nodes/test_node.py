import bgl
import bpy
from gpu_extras.presets import draw_circle_2d

from .. import categories
from .. import events
from ..base_types.node import ProceduralTextureNode
from ..data import buffer as buffer_manager
from ..registration import register_node
from ..sockets.buffer_socket import BufferSocket
from ..util.gl_util import OffscreenRender2DShader


def dimensions_changed(node: 'TestNode', context: bpy.types.Context):
    buffer_manager.replace_instance(
        key=node.buffer_id,
        buffer_type=bgl.GL_BYTE,
        dimensions=4 * node.image_width * node.image_height
    )
    events.node_property_update(node, context)


@register_node(category=categories.test_nodes)
class TestNode(ProceduralTextureNode):
    bl_idname = 'ProceduralTexture_Test'
    bl_label = 'Test Node'

    image_width: bpy.props.IntProperty(default=1024, min=1, update=dimensions_changed)
    image_height: bpy.props.IntProperty(default=1024, min=1, update=dimensions_changed)

    buffer_id: bpy.props.IntProperty(default=-1)

    def init(self, context: bpy.types.Context):
        self.buffer_id = buffer_manager.new_instance(
            buffer_type=bgl.GL_BYTE,
            dimensions=4 * self.image_width * self.image_height
        )
        self.outputs.new(BufferSocket.bl_idname, name='Output')
        super().init_post()

    def draw_buttons(self, context, layout):
        layout.prop(self, 'image_width', text='Width')
        layout.prop(self, 'image_height', text='Height')

    def recalculateOutputs(self):
        buffer_output: BufferSocket = self.outputs.get('Output')
        buffer_output.set_buffer_id(self.buffer_id)
        buffer_output.width = self.image_width
        buffer_output.height = self.image_height
        if self.buffer_id is not -1:
            fragment_shader = '''
in vec2 uvInterp;

void main()
{
    gl_FragColor = vec4(uvInterp, 1.0, 1.0);
}
'''
            with OffscreenRender2DShader(self.image_width, self.image_height, fragment_shader=fragment_shader) as offscreen:
                offscreen.draw_shader()

                buffer = buffer_manager.get_instance(self.buffer_id)
                bgl.glReadBuffer(bgl.GL_BACK)
                bgl.glReadPixels(0, 0, self.image_width, self.image_height, bgl.GL_RGBA, bgl.GL_UNSIGNED_BYTE, buffer)

    def free(self):
        buffer_manager.free_instance(self.buffer_id)
