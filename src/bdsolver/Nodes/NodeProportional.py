
from .NodeBlock import NodeBlock

class NodeProportional(NodeBlock):
    typeString = "proportional"

    def __init__(self, nodeId: str, **kwargs):
        self._k = kwargs["k"]
        super().__init__(nodeId, equation=f"{self._k}*s", **kwargs)
