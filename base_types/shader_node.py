# Copyright (C) 2019 Adrian Guerra
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see https://www.gnu.org/licenses/.

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
    def init_node(self, context: bpy.types.Context):
        super().init_node(context)
        self.outputs.new(BufferSocket.bl_idname, name='Output')

    def setup_buffer(self, new_buffer=False):
        buffer_socket: BufferSocket = self.outputs.get('Output')
        if not buffer_socket.has_buffer() or new_buffer:
            buffer_socket.buffer_id = buffer_manager.new_instance(
                buffer_type=bgl.GL_BYTE,
                dimensions=4 * buffer_socket.width * buffer_socket.height
            )
        else:
            buffer_manager.replace_instance(
                key=buffer_socket.buffer_id,
                buffer_type=bgl.GL_BYTE,
                dimensions=4 * buffer_socket.width * buffer_socket.height
            )

    def draw_buttons(self, context, layout):
        super().draw_buttons(context, layout)
        buffer_socket: BufferSocket = self.outputs.get('Output')
        layout.label(text=f'buffer #{buffer_socket.buffer_id}')
        layout.prop(buffer_socket, 'width', text='Width')
        layout.prop(buffer_socket, 'height', text='Height')

    def copy(self, node: 'ShaderNode'):
        self.is_dirty = True
        self.setup_buffer(new_buffer=True)

    def recalculateOutputs(self):
        super().recalculateOutputs()
        buffer_socket: BufferSocket = self.outputs.get('Output')
        if not buffer_socket.has_buffer():
            self.setup_buffer()
        with OffscreenRendering(buffer_socket.width, buffer_socket.height) as offscreen:
            shader = gpu.types.GPUShader(
                '''\
in vec2 pos;
in vec2 in_uv;

out vec2 uv;

void main()
{
uv = in_uv;
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
                    "in_uv": ((0, 0), (1, 0), (1, 1), (0, 1)),
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

            self.add_shader_inputs(shader)

            batch.draw(shader)

            for texture_id in textures_to_delete:
                bgl.glDeleteTextures(1, texture_id)

            buffer = buffer_socket.get_buffer()
            bgl.glReadBuffer(bgl.GL_BACK)
            bgl.glReadPixels(0, 0, buffer_socket.width, buffer_socket.height, bgl.GL_RGBA, bgl.GL_UNSIGNED_BYTE, buffer)

    def add_shader_inputs(self, shader: 'gpu.types.GPUShader'):
        pass

    def free(self):
        buffer_socket: BufferSocket = self.outputs.get('Output')
        buffer_manager.delete_instance(buffer_socket.buffer_id)

    def load(self):
        self.is_dirty = True
        self.setup_buffer(new_buffer=True)
