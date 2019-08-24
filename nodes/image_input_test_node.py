import bgl
import bpy
import gpu

from ..base_types.shader_node import ShaderNode
from ..registration import register_node
from .. import categories
from ..sockets.buffer_socket import BufferSocket


@register_node(category=categories.test_nodes)
class ImageInputTestNode(ShaderNode):
    bl_idname = 'ProceduralTexture_ImageInputTest'
    bl_label = 'Image Input Test'

    fragment_shader = '''\
in vec2 uvInterp;

uniform sampler2D input_image;

layout(location = 0) out vec4 frag_color;

void main(){
    frag_color = texture(input_image, uvInterp);
}
'''

    def init_node(self, context: bpy.types.Context):
        super().init_node(context)
        self.inputs.new(BufferSocket.bl_idname, 'Input Image', identifier='input_image')

    def add_shader_inputs(self, shader: gpu.types.GPUShader):
        super().add_shader_inputs(shader)
        # input_image_0: 'BufferSocket' = self.inputs['Input Image']
        # if input_image_0.get_buffer() is None:
        #     return
        # print(self._gl_texture_ids[0])
        # bgl.glBindTexture(bgl.GL_TEXTURE_2D, self._gl_texture_ids[0])
        # bgl.glTexParameteri(bgl.GL_TEXTURE_2D, bgl.GL_TEXTURE_MIN_FILTER, bgl.GL_NEAREST)
        # bgl.glTexImage2D(
        #     bgl.GL_TEXTURE_2D,  # target texture
        #     0,  # level of detail
        #     bgl.GL_RGBA,  # 'internal format'
        #     input_image_0.get_width(),  # width
        #     input_image_0.get_height(),  # height
        #     0,  # border width
        #     bgl.GL_RGBA,  # data format
        #     bgl.GL_UNSIGNED_BYTE,  # data type
        #     input_image_0.get_buffer()  # buffer
        # )
        # bgl.glActiveTexture(bgl.GL_TEXTURE0 + 0)
        # bgl.glBindTexture(bgl.GL_TEXTURE_2D, self._gl_texture_ids[0])
        # shader.uniform_int('input_image', 0)
