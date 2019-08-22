import nodeitems_utils
from typing import TYPE_CHECKING, Type

if TYPE_CHECKING:
    from .categories import ProceduralTextureNodeCategory
    from .base_types.node import ProceduralTextureNode

classes_to_register = set()
node_categories_to_register = []


def _fix_property_inheritance(cls):
    # give properties of superclasses to class
    # TODO make this less ugly
    annotations = {}
    for a in reversed(cls.mro()):
        if '__annotations__' in dir(a):
            for k, v in a.__annotations__.items():
                # check if annotation is a property annotation
                if isinstance(v, tuple) and len(v) == 2 and v[0].__module__ == 'bpy.props':
                    annotations[k] = v
    if len(annotations) > 0:
        cls.__annotations__ = annotations


def register_class(cls):
    _fix_property_inheritance(cls)
    classes_to_register.add(cls)
    return cls


def register_node(category: 'ProceduralTextureNodeCategory'):
    def decorator(cls: 'Type[ProceduralTextureNode]'):
        _fix_property_inheritance(cls)
        category.append(nodeitems_utils.NodeItem(cls.bl_idname))
        classes_to_register.add(cls)
        return cls

    return decorator
