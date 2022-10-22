from typing import Any
from matplotlib import pyplot as plt

from graph_helper_functions import generate_graphs
from algorithms import run_algorithms

import os

def evaluate(algo_name: str, results: list, name) -> Any:
    sum_matching = 0
    matchings = list()
    plot_matching = list()
    times = list()
    sum_time = 0
    plot_time = list()
    counter = 1

    for result in results:
        sum_matching += result["MatchingSize"]
        matchings.append(result["MatchingSize"])
        plot_matching.append(sum_matching/counter)
        sum_time += result["Time"]
        times.append(result["Time"])
        plot_time.append(sum_time/counter)
        counter += 1

    with open(f"evaluation/{name}/{algo_name}.txt", "wb") as f:
        f.writelines([
            f"=== {algo_name} ===\n".encode('ascii'),
            "==== Matching ====\n".encode('ascii'),
            f"Average Matching = {sum_matching/len(results)}\n".encode('ascii'),
            f"Maximum Matching = {max(matchings)}, reached {matchings.count(max(matchings))} amount of times.\n".encode('ascii'),
            f"Minimum Matching = {min(matchings)}, reached {matchings.count(min(matchings))} amount of times.\n\n".encode('ascii'),
            "==== Time ====\n".encode('ascii'),
            f"average Time = {round(sum_time/len(results), 6)} ms\n".encode('ascii'),
            f"Maximum Time = {max(times)} ms, reached {times.count(max(times))} amount of times.\n".encode('ascii'),
            f"Minimum Time = {min(times)} ms, reached {times.count(min(times))} amount of times.\n".encode('ascii')]
        )

    return plot_matching, plot_time

def main():
    number_of_iterations = int(input("Number of iterations: "))
    evaluation_name = input("Name of evaluation: ")
    results_networkx = list()
    results_sorted_greedy = list()
    results_multiple_sort = list()

    print("Generating Graphs")
    generate_graphs(number_of_iterations, dir=f"{evaluation_name}/")
    print("Starting Algorithims")
    for i in range(number_of_iterations):
        if i % 100 == 0:
            print(f"Start iteration {i}", flush=True)
        result = run_algorithms(f"random_graph_{i + 1}", dir=f"{evaluation_name}/")
        results_networkx.append(result["Networkx"])
        results_sorted_greedy.append(result["SortedGreedy"])
        results_multiple_sort.append(result["MultipleSortGreedy"])

    if not os.path.exists(f"evaluation/{evaluation_name}"):
        os.makedirs(f"evaluation/{evaluation_name}")

    print("Starting Evaluation")
    networkx_plot_matching,networkx_plot_time  = evaluate("Networkx", results_networkx, evaluation_name)
    sorted_greedy_plot_matching,sorted_greedy_plot_time = evaluate("SortedGreedy", results_sorted_greedy, evaluation_name)
    multiple_sort_plot_matching,multiple_sort_plot_time = evaluate("MultipleSort", results_multiple_sort, evaluation_name)

    y = range(number_of_iterations)
    plt.plot(y, networkx_plot_matching, color='r', label="Networkx")
    plt.plot(y, sorted_greedy_plot_matching, color='g', label="SortedGreedy")
    plt.plot(y, multiple_sort_plot_matching, color='b', label="MultipleSort")
    plt.xlabel("Number of iterations")
    plt.ylabel("Average matching size")
    plt.legend()
    plt.savefig(f'evaluation/{evaluation_name}/matching.png')
    plt.clf()

    plt.plot(y, networkx_plot_time, color='r', label="Networkx")
    plt.plot(y, sorted_greedy_plot_time, color='g', label="SortedGreedy")
    plt.plot(y, multiple_sort_plot_time, color='b', label="MultipleSort")
    plt.xlabel("Number of iterations")
    plt.ylabel("Average Time in Milliseconds")
    plt.legend()
    plt.savefig(f'evaluation/{evaluation_name}/time.png')



if __name__ == "__main__":
    main()