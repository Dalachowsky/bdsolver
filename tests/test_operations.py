
import os
import pytest
from src.bdsolver.BlockDiagram import BlockDiagram
from src.bdsolver.Optimization import DiagramOptimizer

TEST_OPERATIONS_DIR = "./tests/operations"

def basic_test_cases():
    search_dir = TEST_OPERATIONS_DIR + "/basic/"
    for file in os.listdir(search_dir):
        if file.startswith("test_") and not file.endswith("post.yaml"):
            yield search_dir + file

@pytest.mark.parametrize('file', basic_test_cases())
def test_basic_operations(file):
    optimizer = DiagramOptimizer()
    diagram = BlockDiagram()
    with open(file, 'r') as f:
        diagram.fromYaml(f.read())
    diagram_expected = BlockDiagram()
    with open(file.replace(".yaml", "_post.yaml"), 'r') as f:
        diagram_expected.fromYaml(f.read())
    
    diagram_post = optimizer.optimize(diagram)    

    assert diagram_post == diagram_expected
    