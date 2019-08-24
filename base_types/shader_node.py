import bgl
import bpy
import gpu
import gpu_extras

from ..base_types.node import ProceduralTextureNode
from ..data import buffer_manager
from ..sockets.buffer_socket import BufferSocket
from ..sockets.basic_sockets import FloatSocket, IntSocket
from ..util.gl_util import OffscreenRendering
from .. import events


def dimensions_changed(node: 'ShaderNode', context: bpy.types.Context):
    node.setup_buffer()
    events.node_property_update(node, context)


class ShaderNode(ProceduralTextureNode):
    image_width: bpy.props.IntProperty(default=1024, min=1, update=dimensions_changed)
    image_height: bpy.props.IntProperty(default=1024, min=1, update=dimensions_changed)

    buffer_id: bpy.props.IntProperty(default=-1)

    def init_node(self, context: bpy.types.Context):
        super().init_node(context)

        self.outputs.new(BufferSocket.bl_idname, name='Output')

    def setup_buffer(self, reset=False):
        if self.buffer_id == -1 or reset:
            self.buffer_id = buffer_manager.new_instance(
                buffer_type=bgl.GL_BYTE,
                dimensions=4 * self.image_width * self.image_height
            )
        else:
            buffer_manager.replace_instance(
                key=self.buffer_id,
                buffer_type=bgl.GL_BYTE,
                dimensions=4 * self.image_width * self.image_height
            )

    def draw_buttons(self, context, layout):
        super().draw_buttons(context, layout)
        layout.prop(self, 'image_width', text='Width')
        layout.prop(self, 'image_height', text='Height')

    def recalculateOutputs(self):
        super().recalculateOutputs()
        buffer_output: BufferSocket = self.outputs.get('Output')
        buffer_output.set_buffer_id(self.buffer_id)
        buffer_output.width = self.image_width
        buffer_output.height = self.image_height
        if self.buffer_id is not -1:
            with OffscreenRendering(self.image_width, self.image_height) as offscreen:

                shader = gpu.types.GPUShader(
                    '''\
in vec2 pos;
in vec2 uv;

out vec2 uvInterp;

void main()
{
    uvInterp = uv;
    gl_Position = vec4(pos, 0.0, 1.0);
}
''',
                    type(self).fragment_shader
                )

                batch = gpu_extras.batch.batch_for_shader(
                    shader,
                    'TRI_FAN',
                    {
                        "pos": ((-1, -1), (1, -1), (1, 1), (-1, 1)),
                        "uv": ((0, 0), (1, 0), (1, 1), (0, 1)),
                    }
                )

                shader.bind()

                textures_to_delete = []
                texture_count = 0
                for ipt in self.inputs:
                    ipt: 'bpy.types.NodeSocket'
                    if isinstance(ipt, BufferSocket):
                        if not ipt.has_buffer():
                            continue
                        tex_id_buff = bgl.Buffer(bgl.GL_INT, 1)
                        bgl.glGenTextures(1, tex_id_buff)
                        bgl.glActiveTexture(bgl.GL_TEXTURE0 + texture_count)
                        bgl.glBindTexture(bgl.GL_TEXTURE_2D, tex_id_buff[0])
                        bgl.glTexParameteri(bgl.GL_TEXTURE_2D, bgl.GL_TEXTURE_MIN_FILTER, bgl.GL_NEAREST)
                        bgl.glTexImage2D(
                            bgl.GL_TEXTURE_2D,  # target texture
                            0,  # level of detail
                            bgl.GL_RGBA,  # 'internal format'
                            ipt.get_width(),  # width
                            ipt.get_height(),  # height
                            0,  # border width
                            bgl.GL_RGBA,  # data format
                            bgl.GL_UNSIGNED_BYTE,  # data type
                            ipt.get_buffer()  # buffer
                        )
                        shader.uniform_int(ipt.identifier, texture_count)
                        texture_count += 1
                        textures_to_delete.append(tex_id_buff)
                    elif isinstance(ipt, FloatSocket):
                        shader.uniform_float(ipt.identifier, ipt.get_value())
                    elif isinstance(ipt, IntSocket):
                        shader.uniform_int(ipt.identifier, ipt.get_value())

                batch.draw(shader)

                for texture_id in textures_to_delete:
                    bgl.glDeleteTextures(1, texture_id)

                buffer = buffer_manager.get_instance(self.buffer_id)
                bgl.glReadBuffer(bgl.GL_BACK)
                bgl.glReadPixels(0, 0, self.image_width, self.image_height, bgl.GL_RGBA, bgl.GL_UNSIGNED_BYTE, buffer)

    def free(self):
        buffer_manager.delete_instance(self.buffer_id)

    def load(self):
        self.is_dirty = True
        self.setup_buffer(reset=True)
