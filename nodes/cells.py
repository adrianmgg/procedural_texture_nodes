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
from ..sockets.basic_sockets import FloatSocket, IntSocket
from ..events import node_property_update
from ..shaders.shader_creator import load_shader_file
from ..util.props import get_enum_prop_number


@register_node(category=categories.noise_nodes)
class Voronoi(ShaderNode):
    bl_idname = 'ProceduralTexture_Node_Noise_Voronoi'
    bl_label = 'Voronoi'

    coloring_enum = [
        ('INTENSITY', 'Intensity', 'Description', 0),
        ('CELLS', 'Cells', 'Description', 1)
    ]

    coloring_mode: bpy.props.EnumProperty(items=coloring_enum, default='INTENSITY', update=node_property_update)

    def init_node(self, context: bpy.types.Context):
        super().init_node(context)
        scale_socket: IntSocket = self.inputs.new(IntSocket.bl_idname, 'Scale', identifier='scale')
        scale_socket.set_default_value(1)

    def add_shader_inputs(self, shader: 'gpu.types.GPUShader'):
        super().add_shader_inputs(shader)
        shader.uniform_int('coloring_mode', get_enum_prop_number(self.coloring_mode, type(self).coloring_enum))

    def draw_buttons(self, context, layout):
        super().draw_buttons(context, layout)
        layout.prop(self, 'coloring_mode')

    fragment_shader = load_shader_file('nodes/noises/cells.frag')
