from typing import Set, List
import networkx
import pickle
import os
import matplotlib.pyplot as pyplot

"""
Constants for Graph generation
"""
nodes : int = 10
probability_of_edge : float = 0.4

def generate_graphs(amount_of_graphs : int = 1) -> None:
    """
    Function which generates the graphs and stores them
    """
    if not os.path.exists("data/"):
        os.makedirs("data")

    if not os.path.exists("images/"):
        os.makedirs("images")


    for i in range(amount_of_graphs):
        graph : networkx.Graph = networkx.gnp_random_graph(nodes, probability_of_edge)
        graph.name = f"random_graph_{i + 1}"

        with open(f"data/{graph.name}", "wb") as f:
            pickle.dump(graph, f)

        # colors for graph visualization
        node_color="#b6cef2"
        edge_color="#1b50a1"

        # create directory for the graph
        image_name = f"images/{graph.name}_initial.pdf"

        pyplot.title("initial graph")
        pos=networkx.spring_layout(graph, seed=1)
        networkx.draw(graph,
            pos,
            node_size=160,
            node_color=node_color,
            edge_color=edge_color,
            font_size=6,
            width=1,
            with_labels=True)
        pyplot.tight_layout()
        pyplot.savefig(image_name)
        pyplot.close()


"""
Colors from example code
"""
unmatched_edge_color = "#1b50a1"
matched_edge_color = "#eb6b34"
node_color = "#b6cef2"
matched_nodes_colors = ["#34eb64",
                        "#e8eb34",
                        "#eb8f34",
                        "#eb34d9",
                        "#eb345f",
                        "#3499eb",
                        "#4710eb",
                        "#e4ebe5",
                        "#71ebe5",
                        "#d6eb34",
                        "#c9eb34",
                        "#D8D56d",
                        "#d5628c",
                        "#37abc6",
                        "#75a738",
                        "#eb34d6"]


def visualize_matched_graph(graph: networkx.Graph, matching: Set, graph_name: str, matching_algorithm: str) -> None:
    edge_colors = list()
    for edge in graph.edges:
        if edge in matching:
            edge_colors.append(matched_edge_color)
        else:
            edge_colors.append(unmatched_edge_color)

        
    graph_name = f"images/{graph_name}_{matching_algorithm}.pdf"
    graph_title = f"Matching size: {len(matching)}\nAlgo step: {matching_algorithm}"

    pyplot.title(graph_title, fontsize=9)
    pos=networkx.spring_layout(graph, seed=1)
    networkx.draw(graph,
            pos=pos,
            node_size=200,
            node_color=node_color,
            edge_color=edge_colors,
            font_size=8,
            width=1,
            with_labels=True)

    colored = list()
    matched_nodes_colors_copy = matched_nodes_colors.copy()
    for node_1 in graph.nodes:
        for node_2 in graph.nodes:
            if (node_1, node_2) in matching:
                if (node_1, node_2) not in colored:
                    # if there are no more colors available,
                    # update the list
                    if len(matched_nodes_colors_copy) == 0:
                        matched_nodes_colors_copy = matched_nodes_colors.copy()
                    # choose a color from the list
                    color = matched_nodes_colors_copy.pop()
                    # update the list of colored nodes
                    colored.append((node_1, node_2))
                    networkx.draw_networkx_nodes(graph,
                                           pos,
                                           nodelist=[node_1, node_2],
                                           node_color=color,
                                           node_size=200,
                                           alpha=0.8)

    pyplot.tight_layout()
    pyplot.axis('off')
    pyplot.savefig(graph_name)
    pyplot.close()


def import_graph(graph_name : str) -> networkx.Graph:
    with open(f"data/{graph_name}", "rb") as f:
        graph = networkx.Graph(pickle.load(f))
    return graph
