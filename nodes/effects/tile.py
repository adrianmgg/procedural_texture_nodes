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

from ... import categories
from ...base_types.shader_node import ShaderNode
from ...registration import register_node
from ...sockets.basic_sockets import FloatSocket, IntSocket
from ...events import node_property_update
from ...shaders.shader_creator import load_shader_file
from ...util.props import get_enum_prop_number
from ...sockets.buffer_socket import BufferSocket


@register_node(category=categories.effects)
class Tile(ShaderNode):
    bl_idname = 'ProceduralTexture_Node_Effect_Tile'
    bl_label = 'Tile'

    def init_node(self, context: bpy.types.Context):
        super().init_node(context)
        scale_socket: IntSocket = self.inputs.new(IntSocket.bl_idname, 'Scale', identifier='scale')
        scale_socket.set_default_value(1)
        input_image_socket: BufferSocket = self.inputs.new(BufferSocket.bl_idname, name='Input', identifier='input_image')

    def add_shader_inputs(self, shader: 'gpu.types.GPUShader'):
        super().add_shader_inputs(shader)

    def draw_buttons(self, context, layout):
        super().draw_buttons(context, layout)

    fragment_shader = load_shader_file('nodes/effects/tile')
