
from . import NodeBase
import sympy

class NodeBlock(NodeBase):
    typeString = "block"

    def __init__(self, nodeId: str, **kwargs):
        super().__init__(nodeId, **kwargs)
        try:
            self._equation = sympy.parse_expr(kwargs["equation"])
        except KeyError:
            raise Exception(f"Field \"equation\" not found in block node {self.stringId}")
        except Exception as e:
            raise Exception(f"Error assigning equation: \"{kwargs['equation']}\". {e}")

    def getEquation(self):
        return self._equation

    def toDict(self) -> dict:
        ret = super().toDict()
        ret["equation"] = str(self._equation)
        return ret

    def __repr__(self):
        ret = super().__repr__()
        ret += f"- Equation: {self._equation}\n"
        return ret

    def compareNode(self, other: NodeBase):
        if super().compareNode(other):
            if isinstance(other, NodeBlock):
                other: NodeBlock
                if other._equation != self._equation:
                    return False
            return True
        return False
