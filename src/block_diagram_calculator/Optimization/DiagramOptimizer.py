
from copy import deepcopy 
from .OptBlockSeries import OptBlockSeries
from .OptBlockParallel import OptBlockParallel
from .OptRemoveUselessSplit import OptRemoveUselessSplit
from ..BlockDiagram import BlockDiagram

class DiagramOptimizer:

    # Optimizations that are always better
    _optimizationsCertain = [
        OptRemoveUselessSplit,
        OptBlockSeries,
        OptBlockParallel
    ]

    def __init__(self):
        pass

    def optimize(self, diagram: BlockDiagram):
        for opt in self._optimizationsCertain:
            tmpDiagram = deepcopy(diagram)
            for node in list(tmpDiagram.getNodes()):
                hasOptimized = opt.do(tmpDiagram, node)        
                if hasOptimized:
                    break
            if hasOptimized:
                tmpDiagram.removeOrphans()
                return tmpDiagram
