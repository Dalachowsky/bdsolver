
import os
import graphviz
import logging
from pathlib import Path
from copy import deepcopy 
from ..Nodes import INode
from ..Exporters import GraphvizExporter
from .IOpt import IOpt
from .OptBlockSeries import OptBlockSeries
from .OptBlockParallel import OptBlockParallel
from .OptRemoveUselessSplit import OptRemoveUselessSplit
from ..BlockDiagram import BlockDiagram

LOG = logging.getLogger(__name__)

class OptimizeStep:

    def __init__(self, id: str, diagram: BlockDiagram, node: INode, op: IOpt):
        self._diagram = deepcopy(diagram)
        self._node = self._diagram.getNodeById(node.stringId)
        self._op = op
        self._id = id
        self._next: List[OptimizeStep] = []
        self._explored = False
        try:
            self._evaluated = self._op.do(self._diagram, self._node)    
        except Exception as e:
            self._evaluated = False

    @property
    def id(self):
        return self._id

    @property
    def op(self):
        return self._op

    @property
    def evaluated(self):
        return self._evaluated

    @property
    def explored(self):
        return self._explored

    @explored.setter
    def explored(self, state: bool):
        self._explored = state

    @property
    def diagram(self):
        return self._diagram

    @property
    def nodeCount(self):
        return len(self._diagram.getNodes())

    def serialize(self, path: str):
        with open(path, 'w') as f:
            f.write(self._diagram.serializeYaml())

    def addChildStep(self, child: "OptimizeStep"):
        self._next.append(child)

    def getChildSteps(self):
        return self._next

class OptimizeStepRoot(OptimizeStep):

    def __init__(self, diagram: BlockDiagram):
        self._diagram = diagram
        self._node = None
        self._op = None
        self._id = "root"
        self._next: List[OptimizeStep] = []
        self._evaluated = True    
        self._explored = False


class DiagramOptimizer:

    # Optimizations that are always better
    _optimizationsCertain = [
        OptRemoveUselessSplit,
        OptBlockSeries,
        OptBlockParallel
    ]

    def __init__(self, **kwargs):
        self.tmpDir = kwargs.get("tmpDir", "./optimization")
        self._steps = []
        Path(self.tmpDir).mkdir(exist_ok=True)

    def _addStep(self, step: OptimizeStep):
        self._steps.append(step)        

    def _tryExploreStep(self,  step: OptimizeStep):
        newSteps: OptimizeStep = []
        LOG.debug(f"Exploring step {step.id}")
        for op in self._optimizationsCertain:
            for node in step.diagram.getNodes():
                newStep = OptimizeStep(f"Op#{len(self._steps) + len(newSteps)}", step.diagram, node, op)
                if newStep.evaluated:
                    newStep.diagram.removeOrphans()
                    newSteps.append(newStep)
                    e = GraphvizExporter(newStep.diagram)
                    newStep.serialize(f"{self.tmpDir}/config_{newStep.id}.yaml")
                    e.export(f"{self.tmpDir}/{newStep.id}.dot")
        LOG.debug(f"Explored {len(newSteps)} new steps")
        step.explored = True
        return newSteps

    def _optimizeIteration(self):
        newSteps = []
        iterationSteps = [*self._steps]
        for step in iterationSteps:
            if step.explored:
                LOG.debug(f"Step {step.id} already explored")
                continue
            LOG.info(f"Exploring step {step.id}")
            newSteps = self._tryExploreStep(step)
            if len(newSteps) > 0:
                LOG.info(f"Step {step.id} explored")
            for s in newSteps:
                step.addChildStep(s)
                self._addStep(s)

    def getBestDiagram(self):
        bestStep = None
        for step in self._steps:
            if bestStep == None:
                bestStep = step
            if step.nodeCount < bestStep.nodeCount:
                bestStep = step
        return bestStep.diagram

    def optimize(self, diagramSrc: BlockDiagram, maxDepth = 10):
        diagram = deepcopy(diagramSrc)
        rootStep = OptimizeStepRoot(diagram)
        self._steps = [rootStep]
        e = GraphvizExporter(diagram)
        with open(f"{self.tmpDir}/root.yaml", 'w') as f:
            f.write(diagram.serializeYaml())
        e.export(f"{self.tmpDir}/root.dot")

        for i in range(0, maxDepth):
            self._optimizeIteration()
            LOG.debug(f"Optimize iteration {i} finished")

        return self.getBestDiagram()

    def optimizeStep(self, diagram: BlockDiagram):
        for opt in self._optimizationsCertain:
            tmpDiagram = deepcopy(diagram)
            for node in list(tmpDiagram.getNodes()):
                hasOptimized = opt.do(tmpDiagram, node)        
                if hasOptimized:
                    break
            if hasOptimized:
                tmpDiagram.removeOrphans()
                return tmpDiagram

    def printDiagram(self, path = None):
        graph = graphviz.Digraph("Optimization steps")

        for step in self._steps:
            if step.explored:
                nodeColor = "black"
            else:
                nodeColor = "red"
            graph.node(step.id, color=nodeColor)
            for child in step.getChildSteps():
                graph.edge(step.id, child.id, f"{child.op.__name__}\n{child._node.stringId}")

        if path is None:
            path = f"{self.tmpDir}/steps.dot"
        graph.render(path)
