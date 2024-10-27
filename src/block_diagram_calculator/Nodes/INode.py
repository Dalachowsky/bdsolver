
from abc import ABC, abstractmethod

class INode(ABC):

    typeString = ""
    stringId = ""

    @abstractmethod
    def reconnectInputNode(self, nodeOld: "INode", nodeNew: "INode"):
        pass

    @abstractmethod
    def reconnectOutputNode(self, nodeOld: "INode", nodeNew: "INode"):
        pass

    @abstractmethod
    def getInputNodes(self):
        pass

    @abstractmethod
    def getOutputNodes(self):
        pass

    @abstractmethod
    def setInputNode(self, node: "INode", **kwargs):
        pass

    def addInputNode(self, node: "INode", **kwargs):
        pass

    @abstractmethod
    def removeInputNode(self, node: "INode"):
        pass

    @abstractmethod
    def setOutputNode(self, node: "INode", **kwargs):
        pass

    @abstractmethod
    def addOutputNode(self, node: "INode", **kwargs):
        pass

    @abstractmethod
    def removeOutputNode(self, node: "INode"):
        pass
