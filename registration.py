import nodeitems_utils
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .categories import ProceduralTextureNodeCategory
    from .base_types.node import ProceduralTextureNode

classes_to_register = set()
node_categories_to_register = []


def register_class(cls):
    classes_to_register.add(cls)
    return cls


def register_node(category: 'ProceduralTextureNodeCategory'):
    def decorator(cls: 'ProceduralTextureNode'):
        category.append(nodeitems_utils.NodeItem(cls.bl_idname))
        classes_to_register.add(cls)
        return cls
    return decorator
