from typing import TYPE_CHECKING

from bpy.types import NodeSocket

if TYPE_CHECKING:
    from ..base_types.node import ProceduralTextureNode


class ProceduralTextureNodeSocket(NodeSocket):
    node: 'ProceduralTextureNode'

    def update(self):
        print(f'updating socket {self.name}')
        if self.is_output:
            for link in self.links:
                link.to_socket.update()
        else:  # self is input socket
            self.node.updateNode()
