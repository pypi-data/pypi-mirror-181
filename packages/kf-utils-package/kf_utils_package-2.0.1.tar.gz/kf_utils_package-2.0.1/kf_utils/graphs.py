"""
Methods related with graphs management
"""

from pandas import DataFrame
from rdflib import Graph, query as rdflib_query


def load_graph(file_path: str) -> Graph:
    """
    Returns an instance of Graph from a file

    Example:
    load_graph("/home/test.ttl") -> Graph()

    :param file_path: absolute or relative path of the graph

    :return: Graph loaded
    """
    graph = Graph()
    graph.parse(file_path)
    return graph


def convert_response_query_graph_to_df(result_query: rdflib_query.Result) -> DataFrame:
    """
    Transforms the result of an rdf query using the rdflib library to a dataframe.

    :param result_query: rdflib query result

    :return: transformed query result to a dataframe
    """
    return DataFrame(
        data=([None if x is None else x.toPython() for x in row] for row in result_query),
        columns=[str(x) for x in result_query.vars],
    )
