
import json, logging, sys
from .Nodes import *
from .BlockDiagram import BlockDiagram
from .Exporters import GraphvizExporter
from .Optimization import DiagramOptimizer
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("-d", "--depth", action="store", default=10, required=False, type=int)
args = parser.parse_args(sys.argv[1:])

logging.basicConfig(level=logging.DEBUG)

with open("./config.yaml") as f:
    config = f.read()

diag = BlockDiagram()
diag.fromYaml(config)

print(diag.serializeYaml())

for node in diag.getNodes():
    print(node)

exporter = GraphvizExporter(diag)
exporter.export("./diagram.dot")

opt = DiagramOptimizer()
opt.optimize(diag, args.depth)
opt.printDiagram()

# opt = DiagramOptimizer()
# newDiag = opt.optimize(diag)
# i = 0
# while newDiag is not None:
#     print("\nNodes optimized")
#     exporterTmp = GraphvizExporter(newDiag)
#     exporterTmp.export(f"./diagram{i}.dot")
#     for node in newDiag.getNodes():
#         print(node)
#     newDiag = opt.optimize(newDiag)
#     if newDiag is None:
#         print("Did not optimize")
#     i += 1
# 
