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
from ...base_types.node import ProceduralTextureNode
from ...registration import register_node
from ...sockets.buffer_socket import BufferSocket
from ...events import node_property_update


@register_node(category=categories.io_nodes)
class OutputNode(ProceduralTextureNode):
    bl_idname = 'ProceduralTexture_Node_Output'
    bl_label = 'Output'

    colorspace_enum = [
        ('Filmic Log', 'Filmic Log', '', 0),
        ('Linear', 'Linear', '', 1),
        ('Linear ACES', 'Linear ACES', '', 2),
        ('Non-Color', 'Non-Color', '', 3),
        ('Raw', 'Raw', '', 4),
        ('sRGB', 'sRGB', '', 5),
        ('XYZ', 'XYZ', '', 6),
    ]

    colorspace: bpy.props.EnumProperty(items=colorspace_enum, default='sRGB', update=node_property_update)

    image: bpy.props.PointerProperty(type=bpy.types.Image)

    def init_node(self, context):
        super().init_node(context)
        self.inputs.new(BufferSocket.bl_idname, name='Output Image')
        # self.show_preview = True TODO figure out how to set preview image

    def updateNode(self):
        self.backUpdate()

    def recalculateOutputs(self):
        super().recalculateOutputs()
        if self.image is None:
            if self.name not in bpy.data.images:
                bpy.data.images.new(
                    name=self.name,
                    width=1024, height=1024,
                )
            self.image = bpy.data.images.get(self.name)
        self.image.colorspace_settings.name = self.colorspace
        if self.image.name != self.name:
            self.image.name = self.name
        buffer_input_socket: BufferSocket = self.inputs.get('Output Image')
        buffer = buffer_input_socket.get_buffer()
        if buffer is not None:
            if self.image.size[0] != buffer_input_socket.get_width() or self.image.size[1] != buffer_input_socket.get_height():
                self.image.scale(buffer_input_socket.get_width(), buffer_input_socket.get_height())

            self.image.pixels = [x / 255 for x in buffer]  # TODO speed this up
            self.image.update()

    def draw_buttons(self, context: bpy.types.Context, layout: bpy.types.UILayout):
        super().draw_buttons(context, layout)
        layout.prop(self, 'colorspace')

    def copy(self, node):
        pass

    def free(self):
        # should the image be removed on free()?
        pass

