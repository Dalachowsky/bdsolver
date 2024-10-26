import json
from . import *

class NodeFactory:

    def __init__(self):
        self._nodeCount = 0

    def fromJson(self, config: dict):
        try:
            newNodeId = self._nodeCount + 1
            nodeType = config["type"]
            if nodeType == NodeSum.typeString:
                return NodeSum(newNodeId)
        except Exception as e:
            raise Exception(f"Parsing JSON failed. {e}")
        finally:
            self._nodeCount += 1

    def fromYaml(self, nodeId: str, config: dict):
        newNode = None
        try:
            newNodeId = self._nodeCount + 1
            nodeType = config["type"]
            if nodeType == NodeBlock.typeString:
                newNode = NodeBlock(nodeId)
            elif nodeType == NodeInput.typeString:
                newNode = NodeInput(nodeId)
            elif nodeType == NodeOutput.typeString:
                newNode = NodeOutput(nodeId)
            elif nodeType == NodeSplit.typeString:
                newNode = NodeSplit(nodeId)
            elif nodeType == NodeSum.typeString:
                newNode = NodeSum(nodeId)
            else:
                raise Exception(f"Unknown node type: {nodeType}")
        except Exception as e:
            raise Exception(f"Parsing YAML failed. {e}")
        self._nodeCount += 1
        return newNode