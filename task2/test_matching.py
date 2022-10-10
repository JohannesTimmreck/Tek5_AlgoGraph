from typing import List
import networkx


def test_matching(graph : networkx.Graph, matching : List) -> bool:
    return networkx.is_matching(graph, matching)