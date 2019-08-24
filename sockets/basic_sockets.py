import bpy

from ..registration import register_class
from ..base_types.socket import ProceduralTextureNodeSocket
from ..util.decorators import get_from_linked
from ..events import socket_property_update


@register_class
class FloatSocket(ProceduralTextureNodeSocket):
    bl_idname = 'ProceduralTexture_Socket_Float'

    value: bpy.props.FloatProperty(default=0, update=socket_property_update)

    def draw(self, context, layout, node, text: str):
        if not self.is_output and not self.is_linked:
            layout.prop(self, 'value', text=text)
        else:
            layout.label(text=text)

    @get_from_linked
    def get_value(self):
        return self.value

    def set_value(self, value: float):
        self.value = value

    def draw_color(self, context, node: 'Node'):
        return (161 / 255, 161 / 255, 161 / 255, 1.0)


@register_class
class IntSocket(ProceduralTextureNodeSocket):
    bl_idname = 'ProceduralTexture_Socket_Int'

    value: bpy.props.IntProperty(default=0, update=socket_property_update)

    def draw(self, context, layout, node, text: str):
        if not self.is_output and not self.is_linked:
            layout.prop(self, 'value', text=text)
        else:
            layout.label(text=text)

    @get_from_linked
    def get_value(self) -> int:
        return self.value

    def set_value(self, value: int):
        self.value = value

    def draw_color(self, context, node: 'Node'):
        return (161 / 255, 161 / 255, 161 / 255, 1.0)