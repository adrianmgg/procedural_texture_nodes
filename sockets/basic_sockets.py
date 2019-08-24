from typing import TypeVar, Generic

import bpy

from ..base_types.socket import ProceduralTextureNodeSocket
from ..events import socket_property_update
from ..registration import register_class
from ..util.decorators import get_from_linked

T = TypeVar('T')


# TODO give this a better name
class BasicSocket(ProceduralTextureNodeSocket, Generic[T]):

    value: T

    def draw(self, context, layout: 'UILayout', node: 'Node', text: str):
        if not self.is_output and not self.is_linked:
            layout.prop(self, 'value', text=text)
        else:
            layout.label(text=text)

    @get_from_linked
    def get_value(self) -> T:
        return self.value

    def set_value(self, value: T):
        self.value = value

    def set_default_value(self, default_value: T):
        self.value = default_value


@register_class
class FloatSocket(BasicSocket[float]):
    bl_idname = 'ProceduralTexture_Socket_Float'

    value: bpy.props.FloatProperty(default=0, update=socket_property_update)

    def draw_color(self, context, node: 'Node'):
        return (161 / 255, 161 / 255, 161 / 255, 1.0)


@register_class
class IntSocket(BasicSocket[int]):
    bl_idname = 'ProceduralTexture_Socket_Int'

    value: bpy.props.IntProperty(default=0, update=socket_property_update)

    def draw_color(self, context, node: 'Node'):
        return (161 / 255, 161 / 255, 161 / 255, 1.0)
