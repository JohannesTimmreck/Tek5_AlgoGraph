from helper import generate_graph, import_graph, visualize_graph
import networkx


def main():
    name = input("Name for Graph: ")
    generate_graph(name)
    graph = import_graph(name)
    eul = list(networkx.eulerian_path(graph))
    line_graph = networkx.line_graph(graph)
    eul_2 = list()
    for node in eul:
        if node in line_graph.nodes():
            eul_2.append(node)
        else:
            eul_2.append((node[1], node[0]))
    visualize_graph(line_graph, [], name, "Line Graph")
    visualize_graph(line_graph, eul_2, name, "Eularian path in Line Graph")


if __name__ == "__main__":
    main()
