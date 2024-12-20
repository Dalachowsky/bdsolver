
from . import INode
from typing import *

class NodeBase(INode):

    maxInputNodes = 0
    maxOutputNodes = 0

    def __init__(self, nodeId: str, **kwargs):
        self._nodeId = nodeId

        self._inputNodes: List[INode] = []
        self._inputNodesConnArgs: Dict[string, List] = {}
        self._outputNodes: List[INode] = []
        self._outputNodesConnArgs: Dict[string, List] = {}

    @property
    def stringId(self):
        return self._nodeId

    @property
    def logId(self):
        return f"{self.stringId}:"

    def getInputConnArgs(self, nodeId: str):
        try:
            return self._inputNodesConnArgs[nodeId]
        except Exception:
            return []

    def getOutputConnArgs(self, nodeId: str):
        try:
            return self._outputNodesConnArgs[nodeId]
        except Exception:
            return []

    def disconnect(self):
        for node in self._inputNodes:
            node.removeOutputNode(self)
        for node in self._outputNodes:
            node.removeInputNode(self)
        self._inputNodes = []
        self._outputNodes = []

    def reconnectInputNode(self, nodeOld: INode, nodeNew: INode):
        if nodeOld not in self._inputNodes:
            raise Exception(f"Node {nodeOld.stringId} not found in {self.stringId}'s input nodes")
        self.removeInputNode(nodeOld)
        nodeOld.removeOutputNode(self)
        self.addInputNode(nodeNew, *self._inputNodesConnArgs[nodeOld.stringId])
        nodeNew.addOutputNode(self)

    def reconnectOutputNode(self, nodeOld: INode, nodeNew: INode):
        if nodeOld not in self._outputNodes:
            return
        self.removeOutputNode(nodeOld)
        nodeOld.removeInputNode(self)
        self.addOutputNode(nodeNew, *self._outputNodesConnArgs[nodeOld.stringId])
        nodeNew.addInputNode(self, *nodeNew.getInputConnArgs(nodeOld.stringId))

    def getInputNodes(self):
        return self._inputNodes

    def getOutputNodes(self):
        return self._outputNodes

    def setInputNode(self, node: INode, *args):
        self._inputNodes = [node]
        self._inputNodesConnArgs[node.stringId] = args

    def addInputNode(self, node: INode, *args):
        if self.maxInputNodes != 0 and len(self._inputNodes) >= self.maxInputNodes:
            raise Exception(f"{self.logId} Exceeded max input nodes count ({self.maxOutputNodes}) for type {self.typeString}")
        self._inputNodes.append(node)
        self._inputNodesConnArgs[node.stringId] = args

    def removeInputNode(self, node: INode):
        self._inputNodes = [n for n in self._inputNodes if n != node]

    def setOutputNode(self, node: INode, *args):
        self._outputNodes = [node]
        self._outputNodesConnArgs[node.stringId] = args

    def addOutputNode(self, node: INode, *args):
        if self.maxOutputNodes != 0 and len(self._outputNodes) >= self.maxOutputNodes:
            raise Exception(f"{self.logId} Exceeded max output nodes count ({self.maxOutputNodes}) for type {self.typeString}")
        self._outputNodes.append(node)
        self._outputNodesConnArgs[node.stringId] = args

    def removeOutputNode(self, node: INode):
        self._outputNodes = [n for n in self._outputNodes if n != node]

    def toDict(self) -> dict:
        ret = {
            "type": self.typeString,
        }
        return ret

    def __repr__(self):
        ret = f"{self.stringId}:\n"
        ret += "- Inputs:\n"
        for node in self._inputNodes:
            ret += f"  - {node.stringId}\n"
        ret += "- Outputs:\n"
        for node in self._outputNodes:
            ret += f"  - {node.stringId}\n"
        return ret

    def compareNode(self, other: "NodeBase"):
        if not all([n.stringId in [_n.stringId for _n in self.getInputNodes()] for n in other.getInputNodes()]):
            return False
        if not all([n.stringId in [_n.stringId for _n in self.getOutputNodes()] for n in other.getOutputNodes()]):
            return False
        return True
