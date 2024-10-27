
from copy import deepcopy 
from .OptBlockSeries import OptBlockSeries
from ..BlockDiagram import BlockDiagram

class DiagramOptimizer:

    # Optimizations that are always better
    _optimizationsCertain = [
        OptBlockSeries
    ]

    def __init__(self):
        pass

    def optimize(self, diagram: BlockDiagram):
        for opt in self._optimizationsCertain:
            tmpDiagram = deepcopy(diagram)
            for node in tmpDiagram.getNodes():
                hasOptimized = opt.do(tmpDiagram, node)        
                if hasOptimized:
                    tmpDiagram.removeOrphans()
                    return tmpDiagram
