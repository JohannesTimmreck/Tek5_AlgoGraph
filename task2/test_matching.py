from typing import List, Any
import networkx


def test_valid_matching(graph : networkx.Graph, matching : List) -> bool:
    return networkx.is_matching(graph, matching)

def test_maximal_matching(graph : networkx.Graph, matching : List) -> bool:
    return networkx.is_maximal_matching(graph, matching)

def test_maximum_matching(graph : networkx.Graph, matching : List) -> bool:
    return networkx.is_perfect_matching(graph, matching)

def test_matching(graph : networkx.Graph, matching : List) -> Any:
    if not test_valid_matching(graph, matching):
        return None
    if test_maximum_matching(graph, matching):
        return "Maximum"
    if test_maximal_matching(graph, matching):
        return "Maximal"
    return "Valid"
