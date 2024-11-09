
from typing import *
from . import INode, NodeBase

class NodeSum(NodeBase):

    maxInputNodes = 0
    maxOutputNodes = 1
    typeString = "sum"

    def __init__(self, nodeId: int, **kwargs):
        super().__init__(nodeId)
        # Dict of stringId: sign
        self._input_signs: Dict[string, bool] = {}

    def _parseConnectionArgs(self, node: INode, *args):
        try:
            if args[0] == '+':
                sign = True
            elif args[0] == '-':
                sign = False
            else:
                raise Exception(f"Node {node.stringId} has invalid sign {args[0]} expected +/-")
            self._input_signs[node.stringId] = sign
        except IndexError:
            raise Exception(f"Sign not provided for node {self.stringId} input")

    def reconnectInputNode(self, nodeOld: INode, nodeNew: INode):
        super().reconnectInputNode(nodeOld, nodeNew)
        self._input_signs[nodeNew.stringId] = self._input_signs[nodeOld.stringId]

    def setInputNode(self, node: INode, *args):
        super().setInputNode(node, *args)
        self._parseConnectionArgs(node, *args)

    def addInputNode(self, node: INode, *args):
        super().addInputNode(node, *args)
        self._parseConnectionArgs(node, *args)

    def removeInputNode(self, node: INode):
        super().removeInputNode(node)

    def getInputSign(self, node: INode):
        if self._input_signs[node.stringId]:
            return "+"
        else:
            return "-"
