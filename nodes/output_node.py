import bpy
from ..base_types.node import ProceduralTextureNode
from ..registration import register_node
from .. import categories
from ..sockets.image_socket import ImageSocket


@register_node(category=categories.io_nodes)
class OutputNode(ProceduralTextureNode):
    '''Description'''  # TODO
    bl_idname = 'ProceduralTexture_Node_Output'
    bl_label = 'Output'
    bl_icon = 'NODE'  # TODO what is the icon even for?

    image_name: bpy.props.StringProperty()

    def __init__(self):
        self.image_input = None
        self.test = None

    def init(self, context):
        self.inputs: bpy.types.NodeInputs
        self.image_input = self.inputs.new(ImageSocket.bl_idname, 'Output Image', identifier='image_input')
        self.test = self.inputs.new('NodeSocketFloat', 'test')

    def update(self):
        print(self.inputs['Output Image'])

    def draw_buttons(self, context, layout: bpy.types.UILayout):
        layout.label(text='image name')
        layout.prop(self, 'image_name', text='')  # TODO prop name cutting off?

    def copy(self, node):
        pass  # TODO

    def free(self):
        pass
