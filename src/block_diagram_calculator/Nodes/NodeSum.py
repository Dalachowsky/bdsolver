
from . import NodeBase

class NodeSum(NodeBase):

    maxInputNodes = 0
    maxOutputNodes = 1
    typeString = "sum"

    def __init__(self, nodeId: int, **kwargs):
        super().__init__(nodeId)
