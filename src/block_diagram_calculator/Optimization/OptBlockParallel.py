
import logging
from typing import *
from . import IOpt
from ..BlockDiagram import BlockDiagram
from ..Nodes import *

LOG = logging.getLogger(__name__)

class OptBlockParallel(IOpt):

    # Returns tuple of first found parallel blocks. 
    def _findParallelBlocks(start: NodeSplit):
        # Find all connected block nodes
        blockNodes: List[NodeBlock] = [n for n in start.getOutputNodes() if isinstance(n, NodeBlock)]
        # Filter out all block nodes that are not connected to another split node
        blockNodes = [b for b in blockNodes if isinstance(b.getOutputNodes()[0], NodeSplit) ]
        for b1 in blockNodes:
            for b2 in blockNodes:
                if b2 == b1:
                    continue
                if b2.getOutputNodes()[0] == b1.getOutputNodes()[0]:
                    return (b1, b2)


    def do(diagram: BlockDiagram, node: INode):
        if isinstance(node, NodeSplit):
            node: NodeSplit
            blockPair = OptBlockParallel._findParallelBlocks(node)
            if blockPair == None:
                return False

            b1 = blockPair[0]
            b2 = blockPair[1]
            endNode = b1.getOutputNodes()[0]

            # Merge nodes
            LOG.info(f"Merging blocks in parallel: {b1.stringId} + {b2.stringId}")
            newId = f"{b1.stringId}_{b2.stringId}"
            newEquation = f"({b1.getEquation()}) + ({b2.getEquation()})"
            mergedNode = NodeBlock(newId, equation=newEquation)

            # Reconnect nodes
            b1.disconnect()
            b2.disconnect()
            node.addOutputNode(mergedNode)
            mergedNode.addInputNode(node)
            endNode.addInputNode(mergedNode)
            mergedNode.addOutputNode(endNode)
            diagram.addNode(mergedNode)
            return True
        else:
            return False