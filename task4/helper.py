from typing import List
import networkx
import pickle
import os
import matplotlib.pyplot as pyplot


nodes : int = 10
probability_of_edge : float = 0.25


def generate_graph(name : str = "") -> None:
    """
    Function which generates the graphs and stores them
    """
    if not os.path.exists(f"data/"):
        os.makedirs(f"data/")

    if not os.path.exists(f"images/{name}"):
        os.makedirs(f"images/{name}")

    counter = 0
    graph : networkx.Graph = networkx.gnp_random_graph(nodes, probability_of_edge, directed=True)
    while not networkx.is_eulerian(graph):
        graph = networkx.gnp_random_graph(nodes, probability_of_edge)
        counter += 1
    print(f"Amount of generated graphs before reached eularian graph: {counter}")

    with open(f"data/{name}", "wb") as f:
        pickle.dump(graph, f)

    visualize_graph(graph, [], name, "InitialGraph")


edge_color = "#1b50a1"
path_edge_color = "#eb6b34"
node_color = "#b6cef2"
start_node_color = "#34eb64"
end_node_color = "#e8eb34"

def visualize_graph(graph : networkx.Graph, path: List, dir: str,  name: str):
    prev_node = path[0] if len(path) > 1 else None
    path_egdes = list()
    for node in path[1:]:
        path_egdes.append((prev_node, node))
        path_egdes.append((node, prev_node))
        prev_node = node
    
    edge_colors = list()
    for edge in graph.edges:
        if edge in path_egdes:
            edge_colors.append(path_edge_color)
        else:
            edge_colors.append(edge_color)

    graph_name = f"images/{dir}/{name}.pdf"

    pyplot.title(name, fontsize=9)
    pos=networkx.circular_layout(graph)
    networkx.draw(graph,
            pos=pos,
            node_size=200,
            node_color=node_color,
            edge_color=edge_colors,
            font_size=8,
            width=1,
            with_labels=True)
    if len(path) > 1:
        networkx.draw_networkx_nodes(graph,
            pos,
            nodelist=[path[0]],
            node_color=start_node_color,
            node_size=200,
            alpha=0.8)
        networkx.draw_networkx_nodes(graph,
            pos,
            nodelist=[path[-1]],
            node_color=end_node_color,
            node_size=200,
            alpha=0.8)
    pyplot.tight_layout()
    pyplot.axis('off')
    pyplot.savefig(graph_name)
    pyplot.close()
    return


def import_graph(graph_name : str) -> networkx.MultiGraph:
    with open(f"data/{graph_name}", "rb") as f:
        graph: networkx.Graph = networkx.Graph(pickle.load(f))
    return graph


def main():
    generate_graph("test")

if __name__ == "__main__":
    main()
