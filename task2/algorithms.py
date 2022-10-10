from typing import List 
import networkx

from graph_helper_functions import import_graph, visualize_matched_graph, generate_graphs
from test_matching import test_matching

def networkx_algorithm(graph : networkx.Graph) -> List:

    maximal_matching = networkx.maximal_matching(graph)
    visualize_matched_graph(graph, maximal_matching, f"{graph.name}", "networkx")
    if not test_matching(graph, maximal_matching):
        print("[networkx]: Did not find valid matching")
        return []
    return maximal_matching


def first_algorithm(graph : networkx.Graph) -> List:
    matching = []
    neighbours = []

    nodes = graph.nodes()

    for node in nodes:
        neighbours.append({node: [n for n in graph[node]]})

    print("neighbours")
    for node in neighbours:
        print(node)
    sorted_neighbours = sorted(neighbours, key= lambda node : len(nodes[node]))
    print("sorted_neighbours")
    for node in sorted_neighbours:
        print(node)
    if not test_matching(graph, matching):
        print("[first algorithm]: Did not find valid matching")
        return []
    return matching






























def run_algorithms(graph_name : str) -> None:
    graph = import_graph(graph_name)

    networkx_matching = networkx_algorithm(graph)
    first_matching = first_algorithm(graph)

    print(f"=====================")
    print(f"Matching {graph.name}")
    print(f"Maximal possible matches: {graph.number_of_nodes()/2}")
    print(f"Networkx matches: {len(networkx_matching)}")
    print(f"First algorithm matches: {len(first_matching)}")


generate_graphs(1)
for i in range(1):
    run_algorithms(f"random_graph_{i + 1}")