
from . import INode
from typing import *

class NodeBase(INode):

    maxInputNodes = 0
    maxOutputNodes = 0

    def __init__(self, nodeId: str, **kwargs):
        self._nodeId = nodeId

        self._inputNodes: List[INode] = []
        self._outputNodes: List[INode] = []

    @property
    def stringId(self):
        return self._nodeId

    @property
    def logId(self):
        return f"{self.stringId}:"

    def getInputNodes(self):
        return self._inputNodes

    def getOutputNodes(self):
        return self._outputNodes

    def setInputNode(self, node: INode):
        self._inputNodes = [node]

    def addInputNode(self, node: INode):
        if self.maxInputNodes != 0 and len(self._inputNodes) >= self.maxInputNodes:
            raise Exception(f"{self.logId} Exceeded max input nodes count ({self.maxOutputNodes}) for type {self.typeString}")
        self._inputNodes.append(node)

    def setOutputNode(self, node: INode):
        self._outputNodes = [node]

    def addOutputNode(self, node: INode):
        if self.maxOutputNodes != 0 and len(self._outputNodes) >= self.maxOutputNodes:
            raise Exception(f"{self.logId} Exceeded max output nodes count ({self.maxOutputNodes}) for type {self.typeString}")
        self._outputNodes.append(node)

    def __repr__(self):
        ret = f"{self.stringId}:\n"
        ret += "- Inputs:\n"
        for node in self._inputNodes:
            ret += f"  - {node.stringId}\n"
        ret += "- Outputs:\n"
        for node in self._outputNodes:
            ret += f"  - {node.stringId}\n"
        return ret

