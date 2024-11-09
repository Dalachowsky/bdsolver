
from ..Nodes import INode
from ..BlockDiagram import BlockDiagram
from abc import ABC, abstractmethod

class IOpt:

    @abstractmethod
    def do(diagram: BlockDiagram, node: INode):
        pass
