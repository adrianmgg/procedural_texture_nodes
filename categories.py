from nodeitems_utils import NodeCategory
from . import registration
from .node_tree import ProceduralTextureNodeTree


class ProceduralTextureNodeCategory(NodeCategory):
    @classmethod
    def poll(cls, context):
        return context.space_data.tree_type == ProceduralTextureNodeTree.bl_idname

    def __init__(self, identifier, name, description=''):
        self._items = []
        super().__init__(identifier, name, description, self._items)
        registration.node_categories_to_register.append(self)

    def append(self, node):
        self._items.append(node)

# use an enum for these?
test_nodes = ProceduralTextureNodeCategory(
    identifier='TEST',
    name='Test Category'
)

noise_nodes = ProceduralTextureNodeCategory(
    identifier='NOISE',
    name='Noise'
)

io_nodes = ProceduralTextureNodeCategory(
    identifier='IO',
    name='Input/Output'
)

effects = ProceduralTextureNodeCategory(
    identifier='EFFECTS',
    name='Effects'
)
