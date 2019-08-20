from bpy.types import NodeSocket


class ProceduralTextureNodeSocket(NodeSocket):
    def setValue(self, data):
        pass

    def getValue(self):
        pass

    # TODO give this better name
    def getInputValue(self):
        if not self.is_output and self.is_linked:
            for link in self.links:
                print(link)
        return self.getValue()
