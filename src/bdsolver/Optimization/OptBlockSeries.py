
import logging
from . import IOpt
from ..Nodes import INode, NodeBlock
from ..BlockDiagram import BlockDiagram

LOG = logging.getLogger(__name__)

class OptBlockSeries(IOpt):

    def do(diagram: BlockDiagram, node: INode):
        if isinstance(node, NodeBlock):
            node: NodeBlock
            nextNode = node.getOutputNodes()[0]
            if isinstance(nextNode, NodeBlock):
                nextNode: NodeBlock
                LOG.info(f"Merging blocks in series: {node.stringId} + {nextNode.stringId}")

                # Create merged node
                newId = f"{node.stringId}_{nextNode.stringId}"
                newEquation = f"({node.getEquation()}) * ({nextNode.getEquation()})"
                inputNode = node.getInputNodes()[0]
                outputNode = nextNode.getOutputNodes()[0]
                mergedNode = NodeBlock(
                    newId,
                    equation=newEquation
                    )
                diagram.addNode(mergedNode) 
                LOG.debug(f"New node:\n{mergedNode}")

                # Change node connections
                inputNode.reconnectOutputNode(node, mergedNode)
                outputNode.reconnectInputNode(nextNode, mergedNode)

                node.disconnect()
                nextNode.disconnect()
                mergedNode.setInputNode(inputNode)
                mergedNode.setOutputNode(outputNode)
                return True
        else:
            return False
