import networkx

from graph_helper_functions import import_graph, visualize_matched_graph, generate_graphs

def networkx_algorithm(graph_name : str) -> None:
    graph = import_graph(graph_name)

    maximal_matching = networkx.maximal_matching(graph)
    print(f"=====================")
    print(f"Matching {graph_name}")
    print(f"Maximal possible matches: {graph.number_of_nodes()/2}")
    print(f"Found matches: {len(maximal_matching)}")
    visualize_matched_graph(graph, maximal_matching, graph.name)


generate_graphs(20)
for i in range(20):
    networkx_algorithm(f"random_graph_{i + 1}")