
import logging
from typing import *
from . import IOpt
from ..BlockDiagram import BlockDiagram
from ..Nodes import *

LOG = logging.getLogger(__name__)

class OptRemoveUselessSplit(IOpt):

    def do(diagram: BlockDiagram, node: INode):
        if isinstance(node, NodeSplit):
            node: NodeSplit

            if len(node.getInputNodes()) == 1 and len(node.getOutputNodes()) == 1:
                prevNode = node.getInputNodes()[0]
                nextNode = node.getOutputNodes()[0]

                prevNode.reconnectOutputNode(node, nextNode)
                node.disconnect()
                return True

            return False
