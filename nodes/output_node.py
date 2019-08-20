import bpy
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

    image_width: bpy.props.IntProperty(name='image_width', default=1024, min=1, update=events.nodePropertyChanged)
    image_height: bpy.props.IntProperty(name='image_height', default=1024, min=1, update=events.nodePropertyChanged)
    image_use_alpha: bpy.props.BoolProperty(name='image_use_alpha', default=True, update=events.nodePropertyChanged)
    image_is_data: bpy.props.BoolProperty(name='image_is_data', default=False, update=events.nodePropertyChanged)

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
                    width=self.image_width, height=self.image_height,
                    alpha=self.image_use_alpha, is_data=self.image_is_data,
                    float_buffer=False,  # TODO float buffer option
                )
            self.image = bpy.data.images[self.name]
        if self.image.name != self.name:
            self.image.name = self.name

    def updateNode(self):
        self.updateImage()

    def draw_buttons(self, context: bpy.types.Context, layout: bpy.types.UILayout):
        super().draw_buttons(context, layout)
        layout.prop(self, 'image_width', text='Width')
        layout.prop(self, 'image_height', text='Height')
        layout.prop(self, 'image_use_alpha', text='Alpha')
        layout.prop(self, 'image_is_data', text='Non-Color Data')

    def copy(self, node):
        pass

    def free(self):
        # should the image be removed on free()?
        pass
