
import json, logging
from .Nodes import *
from .BlockDiagram import BlockDiagram
from .Exporters import GraphvizExporter

logging.basicConfig(level=logging.DEBUG)

with open("./config.yaml") as f:
    config = f.read()

diag = BlockDiagram()
diag.fromYaml(config)

for node in diag.getNodes():
    print(node)

exporter = GraphvizExporter(diag)
exporter.export("./diagram.dot")
