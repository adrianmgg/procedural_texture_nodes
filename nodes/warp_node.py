import bpy

from .. import categories
from ..base_types.shader_node import ShaderNode
from ..registration import register_node
from ..sockets.basic_sockets import FloatSocket
from ..sockets.buffer_socket import BufferSocket


@register_node(category=categories.effects)
class WarpNode(ShaderNode):
    bl_idname = 'ProceduralTexture_Node_Warp'
    bl_label = 'Warp'

    fragment_shader = '''\
layout(location = 0) out vec4 out_color;

in vec2 uv;

uniform float strength;
uniform sampler2D input_image;
uniform sampler2D warp;

void main(){
    out_color = texture(
        input_image,
        uv + ((texture(warp, uv).x-0.5)*strength)
    );
}
'''

    def init_node(self, context: bpy.types.Context):
        super().init_node(context)
        self.inputs.new(BufferSocket.bl_idname, 'Input Image', identifier='input_image')
        self.inputs.new(BufferSocket.bl_idname, 'Warp Map', identifier='warp')
        # noinspection PyTypeChecker
        strength: FloatSocket = self.inputs.new(FloatSocket.bl_idname, 'Strength', identifier='strength')
        strength.set_default_value(1)
