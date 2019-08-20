import bpy
import gpu

from .. import categories
from ..base_types.node import ProceduralTextureNode
from ..registration import register_node
from ..sockets.buffer_socket import BufferSocket


@register_node(category=categories.io_nodes)
class OutputNode(ProceduralTextureNode):
    bl_idname = 'ProceduralTexture_Node_Output'
    bl_label = 'Output'

    image: bpy.props.PointerProperty(type=bpy.types.Image)

    def init(self, context):
        self.inputs.new(BufferSocket.bl_idname, name='Output Image')
        # self.show_preview = True TODO figure out how to set preview image
        super().init_post()

    # TODO make this change with name
    # TODO what event triggers when node name changes?
    def recalculateOutputs(self):
        if self.image is None:
            if self.name not in bpy.data.images:
                bpy.data.images.new(
                    name=self.name,
                    width=1024, height=1024,
                )
            self.image = bpy.data.images.get(self.name)
        if self.image.name != self.name:
            self.image.name = self.name
        image_input: BufferSocket = self.inputs.get('Output Image')
        buffer: gpu.types.GPUOffScreen = image_input.get_buffer()
        if buffer is not None:
            if self.image.size != [image_input.get_width(), image_input.get_height()]:  # TODO does this comparison work properly
                self.image.scale(image_input.get_width(), image_input.get_height())

            self.image.pixels = [x / 255 for x in buffer]
            self.image.update()

    def draw_buttons(self, context: bpy.types.Context, layout: bpy.types.UILayout):
        super().draw_buttons(context, layout)

    def copy(self, node):
        pass

    def free(self):
        # should the image be removed on free()?
        pass
