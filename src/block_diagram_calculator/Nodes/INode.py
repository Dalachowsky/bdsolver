
from abc import ABC, abstractmethod

class INode(ABC):

    typeString = ""
    stringId = ""

    @abstractmethod
    def getInputNodes(self):
        pass

    @abstractmethod
    def getOutputNodes(self):
        pass

    @abstractmethod
    def setInputNode(self, node: "INode"):
        pass

    def addInputNode(self, node: "INode"):
        pass

    @abstractmethod
    def setOutputNode(self, node: "INode"):
        pass

    @abstractmethod
    def addOutputNode(self, node: "INode"):
        pass
