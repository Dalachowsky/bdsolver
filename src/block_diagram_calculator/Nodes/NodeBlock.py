
from . import NodeBase

class NodeBlock(NodeBase):
    typeString = "block"

    def __init__(self, nodeId: str, **kwargs):
        super().__init__(nodeId, **kwargs)
        try:
            self._equation = kwargs["equation"]
        except Exception as e:
            raise Exception(f"Field \"equation\" not found in block node {self.stringId}")

    def __repr__(self):
        ret = super().__repr__()
        ret += f"- Equation: {self._equation}\n"
        return ret
