import bpy

from ..data import buffer_manager
from ..registration import register_class
from ..base_types.socket import ProceduralTextureNodeSocket
from ..util.decorators import get_from_linked


@register_class
class BufferSocket(ProceduralTextureNodeSocket):
    bl_idname = 'ProceduralTexture_Socket_Buffer'

    buffer_id: bpy.props.IntProperty(default=-1)
    width: bpy.props.IntProperty(default=1024)
    height: bpy.props.IntProperty(default=1024)

    def set_buffer_id(self, new_id: int):
        self.buffer_id = new_id

    def get_buffer_id(self) -> int:
        return self.buffer_id

    @get_from_linked
    def get_buffer(self):
        return buffer_manager.get_instance(self.buffer_id)

    @get_from_linked
    def get_width(self):
        return self.width

    @get_from_linked
    def get_height(self):
        return self.height

    @get_from_linked
    def get_buffer_type(self):
        return buffer_manager.get_buffer_type(self.buffer_id)

    @get_from_linked
    def has_buffer(self):
        return self.buffer_id != -1

    def draw(self, context, layout, node, text):
        layout.label(text=text)

    def draw_color(self, context, node):
        return (0.78, 0.78, 0.16, 1)  # same as shader nodes color socket
