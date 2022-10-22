from typing import List 
import networkx
import timeit

from graph_helper_functions import import_graph, visualize_matched_graph, generate_graphs
from test_matching import test_matching

def networkx_algorithm(graph : networkx.Graph, visualize : bool = False, dir : str = "") -> List:

    maximal_matching = networkx.maximal_matching(graph)
    matching_validation = test_matching(graph, maximal_matching)
    if not matching_validation:
        if visualize:
            print(f"[{graph.name} | Networkx]: Did not find valid matching.")
        return []
    if visualize:
        visualize_matched_graph(graph, maximal_matching, f"{graph.name}", "networkx", dir)
        print(f"[{graph.name} | Networkx]: Found algorithm is: {matching_validation}")
    return maximal_matching


def sorted_greedy_algorithm(graph : networkx.Graph, visualize : bool = False, dir : str = "") -> List:
    matching = list()
    matched_nodes = list()
    neighbours = list()

    nodes = graph.nodes()

    for node in nodes:
        neighbours.append({"name": node, "neighbours": [n for n in graph[node]]})

    sorted_neighbours = sorted(neighbours, key= lambda node : len(node["neighbours"]))

    for node in sorted_neighbours:
        if not node["name"] in matched_nodes:
            for neighbour in node["neighbours"]:
                if not neighbour in matched_nodes:
                    matching.append((node["name"], neighbour))
                    matched_nodes.append(node["name"])
                    matched_nodes.append(neighbour)
                    break
    matching_validation = test_matching(graph, matching)
    if not matching_validation:
        if visualize:
            print(f"[{graph.name} | Sorted Greedy]: Did not find valid matching.")
        return []
    if visualize:
        visualize_matched_graph(graph, set(matching), f"{graph.name}", "Sorted Greedy", dir)
        print(f"[{graph.name} | Sorted Greedy]: Found algorithm is: {matching_validation}")
    return matching


def multiple_sort_greedy_algorithm(graph : networkx.Graph, visualize : bool = False, dir : str = "") -> List:
    matching = list()
    matched_nodes = list()
    neighbours = list()

    nodes = graph.nodes()
    for node in nodes:
        neighbours.append({"name": node, "neighbours": [n for n in graph[node]]})
        
    unmatched_nodes = sorted(neighbours, key= lambda node : len(node["neighbours"]))

    while len(unmatched_nodes) > 0:
        current_node = unmatched_nodes[0]
        if len(current_node["neighbours"]) > 0:
            neighbour = current_node["neighbours"][0]
            matching.append((current_node["name"], neighbour))
            matched_nodes.append(current_node["name"])
            matched_nodes.append(neighbour)
            unmatched_nodes.remove(current_node)
            unmatched_nodes = [node for node in unmatched_nodes if node["name"] != neighbour]
            for node in unmatched_nodes:
                node["neighbours"] = [neighbour_node for neighbour_node in node["neighbours"] if (neighbour_node != neighbour and neighbour_node != current_node["name"])]
        else:
            unmatched_nodes.remove(current_node)
        unmatched_nodes = sorted(unmatched_nodes, key= lambda node : len(node["neighbours"]))

    matching_validation = test_matching(graph, matching)
    if not matching_validation:
        if visualize:
            print(f"[{graph.name} | Multiple Sort]: Did not find valid matching.")
        return []
    if visualize:
        visualize_matched_graph(graph, set(matching), f"{graph.name}", "Multiple Sort", dir)
        print(f"[{graph.name} | Multiple Sort]: Found algorithm is: {matching_validation}")
    return matching


def run_algorithms(graph_name : str, visualize : bool = False, dir : str = "") -> dict:
    graph = import_graph(f"{dir}{graph_name}")

    network_0 = timeit.default_timer()
    networkx_matching = networkx_algorithm(graph, visualize)
    network_1 = timeit.default_timer()
    sorted_greedy_0 = timeit.default_timer()
    sorted_greedy_matching = sorted_greedy_algorithm(graph, visualize)
    sorted_greedy_1 = timeit.default_timer()
    multiple_sort_greedy_0 = timeit.default_timer()
    multiple_sort_greedy_matching = multiple_sort_greedy_algorithm(graph, visualize)
    multiple_sort_greedy_1 = timeit.default_timer()

    if visualize:
        print(f"=====================")
        print(f"Matching {graph.name}")
        print(f"Maximal possible matches: {graph.number_of_nodes()/2}")
        print(f"Networkx matches: {len(networkx_matching)} | Time: {round((network_1 - network_0) * 10 ** 3, 6)} ms")
        print(f"Sorted Greedy matches: {len(sorted_greedy_matching)} | Time: {round((sorted_greedy_1 - sorted_greedy_0) * 10 ** 3, 6)} ms")
        print(f"Multiple Sort matches: {len(multiple_sort_greedy_matching)} | Time: {round((multiple_sort_greedy_1 - multiple_sort_greedy_0) * 10 ** 3, 6)} ms")

    return {
        "Networkx": {
            "MatchingSize": len(networkx_matching),
            "Time": round((network_1 - network_0) * 10 ** 3, 6)
        },
        "SortedGreedy": {
            "MatchingSize": len(sorted_greedy_matching),
            "Time": round((sorted_greedy_1 - sorted_greedy_0) * 10 ** 3, 6)
        },
        "MultipleSortGreedy": {
            "MatchingSize": len(multiple_sort_greedy_matching),
            "Time": round((multiple_sort_greedy_1 - multiple_sort_greedy_0) * 10 ** 3, 6)
        }
    }


def main():
    amount_of_graphs : int = 1
    generate_graphs(amount_of_graphs, True)
    for i in range(amount_of_graphs):
        run_algorithms(f"random_graph_{i + 1}", True)

if __name__ == "__main__":
    main()