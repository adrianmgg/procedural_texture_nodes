import bpy
import gpu

from .. import categories
from .. import events
from ..base_types.shader_node import ShaderNode
from ..sockets.basic_sockets import FloatSocket, IntSocket
from ..sockets.buffer_socket import BufferSocket
from ..registration import register_node


@register_node(category=categories.effects)
class WarpNode(ShaderNode):
    bl_idname = 'ProceduralTexture_Node_Warp'
    bl_label = 'Warp'

    fragment_shader = '''\
layout(location = 0) out vec4 out_color;

in vec2 uvInterp;

uniform float strength;
uniform sampler2D input_image;
uniform sampler2D warp;

void main(){
    out_color = texture(
        input_image,
        uvInterp + ((texture(warp, uvInterp).x-0.5)*strength)
    );
}
'''

    def init_node(self, context: bpy.types.Context):
        super().init_node(context)
        self.inputs.new(BufferSocket.bl_idname, 'Input Image', identifier='input_image')
        self.inputs.new(BufferSocket.bl_idname, 'Warp Map', identifier='warp')
        self.inputs.new(FloatSocket.bl_idname, 'Strength', identifier='strength')
