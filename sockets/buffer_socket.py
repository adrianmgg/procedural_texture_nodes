import bpy

from ..data import buffer
from ..registration import register_class
from ..base_types.socket import ProceduralTextureNodeSocket
from ..util.decorators import get_from_linked


@register_class
class BufferSocket(ProceduralTextureNodeSocket):
    bl_idname = 'ProceduralTexture_Socket_Buffer'
    bl_label = 'Image'

    buffer_id: bpy.props.IntProperty(default=-1)
    width: bpy.props.IntProperty()
    height: bpy.props.FloatProperty()

    def set_buffer_id(self, new_id: int):
        self.buffer_id = new_id

    def get_buffer_id(self) -> int:
        return self.buffer_id

    def get_buffer(self):
        if not self.is_output and self.is_linked:
            return self.links[0].from_socket.get_buffer()
        return buffer.get_instance(self.buffer_id)

    def get_width(self):
        if not self.is_output and self.is_linked:
            return self.links[0].from_socket.width
        return self.width

    def get_height(self):
        if not self.is_output and self.is_linked:
            return self.links[0].from_socket.height
        return self.height

    def draw(self, context, layout, node, text):
        layout.label(text=text)

    def draw_color(self, context, node):
        return (0.78, 0.78, 0.16, 1)  # same as shader nodes color socket
