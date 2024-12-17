import sys
import os
import argparse
import pathlib

from typing import Dict, Tuple, List, Union, Optional
import orjson
from orjson import JSONDecodeError
import networkx as nx

from setting import *

from helper_script.json_helper import *
from helper_script.file_reader_helper import *
from helper_script.func_timer import SingleTimer, MultipleTimer

from modules_script import m_preprocess_text
from modules_script import m_process_text
from modules_script import m_graph_nx
from modules_script import m_graph_custom


print("==================================")
print()


def get_command_line_arg() -> argparse.ArgumentParser.parse_args:
    """
    Parse command line arguments using argparse
    """
    parser = argparse.ArgumentParser(description="Calculate inverse pagerank from json file")

    parser.add_argument(
        "-f", "--files", 
        nargs='*', 
        help="Calculate only specified json file(s)"
    )

    parser.add_argument(
        "-e", "--exclude",
        nargs='+',
        help="Exclude specified json file(s)" 
    )

    args = parser.parse_args()

    return args


def print_settings() -> None:
    print(f"=== Settings === (Config in setting.py)\n")

    print(f"DATA_DIR\t\t\t: {DATA_DIR}")
    print(f"NLTK_PATH\t\t\t: {NLTK_PATH}")
    print(f"OUTPUT_DIR\t\t\t: {OUTPUT_DIR}")
    print()

    print(f"USE_PAGERANK_LIBRARY\t\t: {USE_PAGERANK_LIBRARY}")
    print(f"OUTPUT_GRAPH\t\t\t: {OUTPUT_GRAPH}")
    print(f"SHOW_GRAPH\t\t\t: {SHOW_GRAPH}")
    print()

    print(f"TARGET_DATA_KEY\t\t\t: {'.'.join(TARGET_DATA_KEY)}")
    print(f"MAX_CALCULATION_THRESHOLD\t: {CALCULATION_THRESHOLD}")
    print(f"MAX_CALCULATION_ITERATION\t: {MAX_CALCULATION_ITERATION}")
    print(f"MAX_TRUST_RANK_ITERATION\t: {MAX_TRUST_RANK_ITERATION}")
    print()


def print_timer(timer: SingleTimer, newline: bool = True) -> None:
    print(f"  ({timer.get_time_and_restart():.2f} ms)")
    if newline:
        print()


def get_all_files_name(dir: str, extension: Optional[List[str]] = None) -> List[str]:
    if extension is not None:
        return [file for file in os.listdir(dir) if os.path.isfile(os.path.join(dir, file)) and pathlib.Path(file).suffix in extension]

    return [file for file in os.listdir(dir) if os.path.isfile(os.path.join(dir, file))]


def processed_text(data_path: str, write_to_output: bool = True, output_path: str = OUTPUT_DIR, logging: bool = False) -> List[Tuple[str, str, int]]:
    
    """
    Preprocesses text data and writes the result to cache.

    Reads a JSON file from the given data path, preprocesses the text data by
    converting it to bigrams, merging multiple bigrams, and converting it to 
    weighted bigrams. The result is written to cache if write_to_output is True.

    Parameters
    ----------
    data_path : str
        The path to the JSON file containing the text data.
    write_to_output : bool, optional
        Whether to write the result to cache. Defaults to True.
    output_path : str, optional
        The path to write the result to. Defaults to OUTPUT_DIR.
    logging : bool, optional
        Whether to print the result. Defaults to False.

    Returns
    -------
    List[Tuple[str, str, int]]
        The preprocessed text data in the form of weighted bigrams.
    """
    print("Preprocessing data")
    # Get raw text data
    all_text_data = read_json(data_path)

    # Preprocess & process text data
    processed_text_data = m_process_text.json_to_bigrams(all_text_data, TARGET_DATA_KEY, throw_key_error=True)

    # Merge multiple text data (list of bigrams)
    processed_text_data = m_process_text.merge_multiple_bigrams_list(processed_text_data, sort=False)

    # Convert to weighted bigrams
    processed_text_data = m_process_text.bigrams_to_weighted_bigrams(processed_text_data, sort=True)

    # Write to cache
    if write_to_output:
        write_to_file(output_path, to_json(processed_text_data, indent=True), overwrite=True)

    return processed_text_data


def calculate_inverse_pagerank(word_graph: Union[nx.DiGraph, m_graph_custom.WeightedWordDiGraph], epsilon: float = CALCULATION_THRESHOLD, max_iter: int = MAX_CALCULATION_ITERATION) -> Dict[str, float]:
    """
    Calculate inverse PageRank scores on a given weighted directed graph.

    Parameters
    ----------
    word_graph : Union[nx.DiGraph, m_graph_custom.WeightedWordDiGraph]
        The weighted directed graph to calculate the scores on.
    max_iter : int, optional
        The maximum number of iterations. Defaults to MAX_CALCULATION_ITERATION.

    Returns
    -------
    Dict[str, float]
        A dictionary mapping each node to its inverse PageRank score.

    Notes
    -----
    Supports two types of weighted directed graph: nx.DiGraph and m_graph_custom.WeightedWordDiGraph.
    """
    inverse_pagerank_scores = None

    if isinstance(word_graph, nx.DiGraph):
        return m_graph_nx.get_inverse_pagerank(word_graph, max_iter=max_iter)

    elif isinstance(word_graph, m_graph_custom.WeightedWordDiGraph):
        return word_graph.get_inverse_pagerank(max_iter=max_iter, epsilon=epsilon)

    else:
        raise TypeError("word_graph must be either nx.DiGraph or m_graph_custom.WeightedWordDiGraph")


def calculate_trust_rank(word_graph: Union[nx.DiGraph, m_graph_custom.WeightedWordDiGraph], sorted_inverse_pagerank_scores: List[Tuple[str, float]], bias_amount: int, epsilon: float = CALCULATION_THRESHOLD, max_iter: int = MAX_TRUST_RANK_ITERATION) -> None:
    if isinstance(word_graph, nx.DiGraph):
        graph = list(word_graph.word_graph.edges(data=True))
        graph = [(n1, n2, p["weight"]) for n1, n2, p in graph]
        word_graph = m_graph_custom.WeightedWordDiGraph(graph)
    
    return word_graph.get_trust_rank(bias_amount, sorted_inverse_pagerank_scores, epsilon=epsilon, max_iter=max_iter)


def calculation_main(data_dir: str, data_name: str) -> None:
    """
    Main calculation function.

    This function reads the json file from the specified directory with the given name,
    preprocesses the text, generates a graph, calculates the inverse pagerank, and writes
    the result to a new json file. If SHOW_GRAPH is set to True, it will also visualize
    the graph.

    Parameters
    ----------
    data_dir : str
        The directory of the json file
    data_name : str
        The name of the json file

    Returns
    -------
    None
    """
    data_path = f"{data_dir}/{data_name}"

    # Time function runtime
    running_timer = MultipleTimer(["func"])
    
    print(f"=== Calculating {data_name} ===\n")
    
    print("* ", end="")
    running_timer.timer["func"].start()
    bigrams_list = processed_text(
        data_path,
        output_path=f"{OUTPUT_DIR}/graph_{data_name}",
        write_to_output=OUTPUT_GRAPH,
        logging=True
    )
    print_timer(running_timer.timer["func"])


    # Generate graph
    print("* Creating graph")
    word_graph: Union[nx.DiGraph, m_graph_custom.WeightedWordDiGraph, None] = None
    if USE_PAGERANK_LIBRARY:
        word_graph = m_graph_nx.generate_graph(bigrams_list, weighted=True)
    else:
        word_graph = m_graph_custom.WeightedWordDiGraph(bigrams_list)
    print(f"  nodes: {len(word_graph.nodes)}, edges: {len(word_graph.edges)}")
    print_timer(running_timer.timer["func"])


    # Inverse-PageRank
    print("* Calculating inverse pagerank")
    inverse_pagerank_scores = calculate_inverse_pagerank(word_graph)
    sorted_inverse_pagerank_scores = m_graph_custom.get_sorted_rank_score(inverse_pagerank_scores)
    print(f"  Sum: {sum(inverse_pagerank_scores.values()): .4f}")  # Verifying
    print_timer(running_timer.timer["func"])
    

    # TODO
    # TrustRank
    print("* Calculating trustrank")
    trust_rank_scores = calculate_trust_rank(word_graph, sorted_inverse_pagerank_scores, bias_amount=TRUST_RANK_BIAS_AMOUNT, max_iter=MAX_TRUST_RANK_ITERATION)
    sorted_trust_rank_scores = m_graph_custom.get_sorted_rank_score(trust_rank_scores)
    print(f"  Sum: {sum(trust_rank_scores.values()): .4f}")  # Verifying
    print_timer(running_timer.timer["func"])


    # Write inverse-PageRank score to file
    print("* Writing to output")
    output_file_name = f"inverse_pagerank_nx_{data_name}" if USE_PAGERANK_LIBRARY else f"inverse_pagerank_custom_{data_name}"
    write_to_file(
        f"{OUTPUT_DIR}/{output_file_name}",
        to_json(sorted_inverse_pagerank_scores, indent=True), 
        overwrite=True
    )

    # Write TrustRank score to file
    write_to_file(
        f"{OUTPUT_DIR}/trust_rank_{data_name}",
        to_json(sorted_trust_rank_scores, indent=True), 
        overwrite=True
    )
    print_timer(running_timer.timer["func"])


    running_timer.main.stop()

    # Visualize graph (if SHOW_GRAPH is set to True)
    if SHOW_GRAPH:
        print("* Visualizing graph")
        m_graph_nx.plot_graph(word_graph, node_size=100, weighted=True, with_labels=False)


def main() -> None:
    # Get command line arguments
    cmd_arg = get_command_line_arg()

    data_file_name = None

    if cmd_arg.files:
        data_file_name = cmd_arg.files
    elif cmd_arg.exclude:
        data_file_name = get_all_files_name(DATA_DIR, [".json"])
        data_file_name = [file for file in data_file_name if file not in cmd_arg.exclude]
    else:
        data_file_name = get_all_files_name(DATA_DIR, [".json"])

    # Print calculating file(s)
    print("=== Running ===\n")
    print("Using networkx library" if USE_PAGERANK_LIBRARY else "Using custom graph", "\n")

    print("Data to calculate:")
    for i, data in enumerate(data_file_name):
        print(f"  {i+1}.) {data}")
    print()

    # Print settings
    print_settings()

    # Start timer
    main_timer = MultipleTimer()

    # Calculate all file(s)
    for i, data in enumerate(data_file_name):
        print(f"({i+1}/{len(data_file_name)}) ", end="")

        # Time each file runtime
        main_timer.newTimer(data)

        try:
            calculation_main(DATA_DIR, data)
        except Exception as e:
            print(f"\nError calculating {data} ({type(e)}): {e}\n")

        main_timer.timer[data].stop()
        print(f"Calculation runtime: {main_timer.timer[data].get_start_to_stop():.2f} ms\n")

    print("\n=== Finished ===\n")


    # Print each runtime & total runtime
    runtime = main_timer.main.get_time_and_restart()


    if runtime < 1e4:
        print(f"Total runtime: {runtime:.2f} ms")
    else:
        print(f"Total runtime: {runtime/1e3:.3f} s")
    print()

    for i, data in enumerate(data_file_name):
        print(f"  {f'{i+1}.) {data}: ':<70} {main_timer.timer[data].get_start_to_stop():.2f} ms")

    print()

    return


if __name__ == "__main__":
    main()