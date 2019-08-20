import bpy
import gpu

from ..base_types.node import ProceduralTextureNode
from ..registration import register_node
from .. import categories
from ..sockets.image_socket import ImageSocket
from .. import events


@register_node(category=categories.io_nodes)
class OutputNode(ProceduralTextureNode):
    '''Description'''  # TODO
    bl_idname = 'ProceduralTexture_Node_Output'
    bl_label = 'Output'
    bl_icon = 'NODE'  # TODO what is the icon even for?

    image: bpy.props.PointerProperty(type=bpy.types.Image)

    # image_width: bpy.props.IntProperty(name='image_width', default=1024, min=1, update=events.nodePropertyChanged)
    # image_height: bpy.props.IntProperty(name='image_height', default=1024, min=1, update=events.nodePropertyChanged)

    def init(self, context):
        self.inputs.new(ImageSocket.bl_idname, name='Output Image')
        # self.show_preview = True TODO figure out how to set preview image
        self.updateImage()

    # TODO make this change with name
    # TODO what event triggers when node name changes?
    def updateImage(self):
        if self.image is None:
            if self.name not in bpy.data.images:
                bpy.data.images.new(
                    name=self.name,
                    width=1024, height=1024,
                )
            self.image = bpy.data.images.get(self.name)
        if self.image.name != self.name:
            self.image.name = self.name
        image_input: ImageSocket = self.inputs.get('Output Image')
        buffer: gpu.types.GPUOffScreen = image_input.get_buffer()
        if buffer is not None:
            if self.image.size != [image_input.get_width(), image_input.get_height()]:  # TODO does this comparison work properly
                self.image.scale(image_input.get_width(), image_input.get_height())

            self.image.pixels = [x / 255 for x in buffer]
            self.image.update()

    def updateNode(self):
        self.updateImage()

    def draw_buttons(self, context: bpy.types.Context, layout: bpy.types.UILayout):
        super().draw_buttons(context, layout)
        # layout.prop(self, 'image_width', text='Width')
        # layout.prop(self, 'image_height', text='Height')

    def copy(self, node):
        pass

    def free(self):
        # should the image be removed on free()?
        pass
