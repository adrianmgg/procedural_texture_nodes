import bgl
import bpy
import gpu

from ..base_types.node import ProceduralTextureNode
from ..data import buffer_manager
from ..sockets.buffer_socket import BufferSocket
from ..util.gl_util import OffscreenRender2DShader
from .. import events


def dimensions_changed(node: 'ShaderNode', context: bpy.types.Context):
    buffer_manager.replace_instance(
        key=node.buffer_id,
        buffer_type=bgl.GL_BYTE,
        dimensions=4 * node.image_width * node.image_height
    )
    events.node_property_update(node, context)


class ShaderNode(ProceduralTextureNode):
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
            with OffscreenRender2DShader(self.image_width, self.image_height, fragment_shader=type(self).fragment_shader) \
                    as offscreen:
                offscreen.shader.bind()
                self.add_shader_inputs(offscreen.shader)
                offscreen.draw_shader()

                buffer = buffer_manager.get_instance(self.buffer_id)
                bgl.glReadBuffer(bgl.GL_BACK)
                bgl.glReadPixels(0, 0, self.image_width, self.image_height, bgl.GL_RGBA, bgl.GL_UNSIGNED_BYTE, buffer)

    def free(self):
        buffer_manager.free_instance(self.buffer_id)

    def add_shader_inputs(self, shader: gpu.types.GPUShader):
        pass
