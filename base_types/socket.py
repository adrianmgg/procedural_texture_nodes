# Copyright (C) 2019 Adrian Guerra
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see https://www.gnu.org/licenses/.

from typing import TYPE_CHECKING

from bpy.types import NodeSocket

if TYPE_CHECKING:
    from ..base_types.node import ProceduralTextureNode


class ProceduralTextureNodeSocket(NodeSocket):
    node: 'ProceduralTextureNode'

    def update(self):
        if self.is_output:
            for link in self.links:
                link.to_socket.update()
        else:  # self is input socket
            if self.node.initialization_completed:
                self.node.updateNode()
