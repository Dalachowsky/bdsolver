
import logging
import graphviz
from ..BlockDiagram import BlockDiagram
from ..Nodes import *

LOG = logging.getLogger(__name__)

class GraphvizExporter:

    def __init__(self, diag: BlockDiagram):
        self._diagram = diag

    def exportNode(self, diagram: graphviz.Graph, node: INode):
        nodeLabel = node.stringId
        nodeShape = "rectangle"
        attrs = {}

        if node.typeString == NodeBlock.typeString:
            pass
        elif node.typeString == NodeInput.typeString:
            nodeShape = "none"
        elif node.typeString == NodeOutput.typeString:
            nodeShape = "none"
        elif node.typeString == NodeSplit.typeString:
            nodeShape = "point"
        elif node.typeString == NodeSum.typeString:
            nodeLabel = "X"
            nodeShape = "circle"

        diagram.node(node.stringId, 
            label=nodeLabel, 
            #xlabel=nodeLabel,  
            shape=nodeShape)

        for outputNode in node.getOutputNodes():
            LOG.debug(f"Drawing connection {node.stringId} -> {outputNode.stringId}")
            diagram.edge(
                node.stringId, 
                outputNode.stringId,
                #headport="w"
            )

    def export(self, path: str):

        diagram = graphviz.Digraph()
        diagram.attr("graph", rankdir="LR")
        diagram.attr("graph", splines="ortho")
        diagram.attr("graph", nodesep="1.8")

        for node in self._diagram.getNodes():
            self.exportNode(diagram, node)

        diagram.render(path)
