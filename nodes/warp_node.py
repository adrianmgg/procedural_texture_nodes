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
        strength: FloatSocket = self.inputs.new(FloatSocket.bl_idname, 'Strength', identifier='strength')
        strength.set_default_value(1)
