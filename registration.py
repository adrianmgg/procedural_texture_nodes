classes_to_register = set()
node_categories_to_register = []
import nodeitems_utils

def register_class(cls):
    classes_to_register.add(cls)
    return cls

def register_node(category):
    def decorator(cls):
        category.append(nodeitems_utils.NodeItem(cls.bl_idname))
        classes_to_register.add(cls)
        return cls
    return decorator