from ..registration import register_class
from ..base_types.socket import ProceduralTextureNodeSocket


@register_class
class ImageSocket(ProceduralTextureNodeSocket):
    '''description'''  # TODO
    bl_idname = 'ProceduralTexture_Socket_Image'
    bl_label = 'Image'

    def draw(self, context, layout, node, text):
        layout.label(text=text)

    def setValue(self, value):
        pass

    def getValue(self):
        pass

    def draw_color(self, context, node):
        return (0.78, 0.78, 0.16, 1)  # same as shader nodes color socket
