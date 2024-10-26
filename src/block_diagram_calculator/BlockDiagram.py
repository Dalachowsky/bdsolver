
import json, yaml
from typing import *
from .Nodes import *

import logging

LOG = logging.getLogger(__name__)

class BlockDiagram:

    def __init__(self):
        self._nodes: Dict[str, INode] = {}
        self._nodeFactory = NodeFactory()

    def getNodes(self) -> List[INode]:
        return self._nodes.values()

    def getNodeById(self, id: str):
        return self._nodes[id]

    def parseConnection(self, connectionStr: str):
        parts = connectionStr.split(' ')
        if len(parts) != 3 or parts[1] != "-":
            raise Exception(f"Wrong format of connection: {connectionStr}")

        node_src_parts = parts[0].split('/') 
        node_dst_parts = parts[2].split('/') 

        node_src_label = node_src_parts[0]
        node_dst_label = node_dst_parts[0]
        node_src_args = node_src_parts[1:]
        node_dst_args = node_dst_parts[1:]

        srcNode = self.getNodeById(node_src_label)
        dstNode = self.getNodeById(node_dst_label)

        LOG.debug(f"{srcNode.stringId}: adding output node {dstNode.stringId}")
        srcNode.addOutputNode(dstNode)
        LOG.debug(f"{dstNode.stringId}: adding input node {srcNode.stringId}")
        dstNode.addInputNode(srcNode)

        LOG.debug(f"Added connection {srcNode.stringId} -> {dstNode.stringId}")

    def fromYaml(self, yamlDoc: str):
        config = yaml.load(yamlDoc, yaml.BaseLoader)
        try:
            nodesConfig = config["nodes"]
        except Exception as e:
            raise Exception("\"nodes\" field not present in config")
        try:
            connectionsConfig = config["connections"]
        except Exception as e:
            raise Exception("\"connections\" field not present in config")

        for nodeId, nodeConfig in nodesConfig.items():
            n = self._nodeFactory.fromYaml(nodeId, nodeConfig)
            self._nodes[nodeId] = n
            print(f"New node: {n.stringId} type: {n.typeString}")

        for connection in connectionsConfig:
            self.parseConnection(connection)

    def fromJson(self, jsonString: str):
        config = json.loads(jsonString)
        try:
            nodesConfig = config["nodes"]
        except Exception as e:
            raise Exception("\"nodes\" field not present in config")

        for node in nodesConfig:
            self._nodes.append(self._nodeFactory.fromJson(node))
