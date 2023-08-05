import os
import unittest

from pandas import DataFrame
from rdflib import Graph

from kf_utils import graphs
from test.resources import test_messages


class TestGraphs(unittest.TestCase):
    """
    Test graphs scripts and methods
    """

    load_graph_method: str = 'graphs.load_graph'
    convert_response_query_graph_to_df_method: str = 'graphs.convert_response_query_graph_to_df'

    pwd = os.path.abspath(os.path.dirname(__file__))

    if pwd.endswith('test'):
        resources_path = os.path.join(
            pwd,
            'resources'
        )
    else:
        resources_path = os.path.join(
            pwd,
            'test'
            'resources'
        )

    def setUp(self) -> None:
        self.graph_example_serialized: Graph = Graph()\
            .parse("http://www.w3.org/People/Berners-Lee/card")\
            .serialize(format="turtle")

    # 1. Test graphs.load_graph
    def test_load_graph_valid_file_path(self) -> None:
        """
        GIVEN a valid file path \n
        WHEN graphs.load_graph method is called \n
        THEN the returned value is not None
        AND the returned value is of type Graph
        AND the graph is correctly loaded \n
        """

        file_path: str = os.path.join(self.resources_path, 'graph_example.ttl')
        graph = graphs.load_graph(file_path)
        graph_serialized = graph.serialize(format="turtle")

        self.assertIsNotNone(
            file_path,
            test_messages.METHOD_RETURNS_NONE.format(method=self.load_graph_method)
        )

        self.assertIsInstance(
            graph,
            Graph,
            test_messages.METHOD_RETURNED_VALUE_IS_NOT.format(
                method=self.load_graph_method,
                value='str'
            )
        )

        self.assertEqual(
            graph_serialized,
            self.graph_example_serialized,
            test_messages.IS_NOT_EQUAL.format(
                method=self.load_graph_method,
                first="File graph",
                second="stored graph example")
        )

    # 2. Test graph.convert_response_query_graph_to_df
    def test_convert_response_query_graph_to_df_not_valid_param(self) -> None:
        """
        GIVEN a not valid query param \n
        WHEN graphs.convert_response_query_graph_to_df method is called \n
        THEN an AttributeError exception is raised
        """
        not_valid_param = ['this is not a valid query param']

        self.assertRaises(AttributeError, graphs.convert_response_query_graph_to_df, not_valid_param)

    def test_convert_response_query_graph_to_df_return_type(self) -> None:
        """
        GIVEN a valid query param \n
        WHEN graphs.convert_response_query_graph_to_df method is called \n
        THEN graphs.convert_response_query_graph_to_df returned value is not None \n
        AND graphs.convert_response_query_graph_to_df returned value type is DataFrame
        """

        g = Graph()
        g.parse(
            data="""
                <x:> a <c:> .
                <y:> a <c:> .
            """,
            format="turtle"
        )
        query_result = g.query("""SELECT ?s WHERE { ?s a <c:> }""")
        query_result_to_df = graphs.convert_response_query_graph_to_df(query_result)

        self.assertIsNotNone(
            query_result_to_df,
            test_messages.METHOD_RETURNS_NONE.format(method=self.convert_response_query_graph_to_df_method)
        )
        self.assertIsInstance(
            query_result_to_df,
            DataFrame,
            test_messages.METHOD_RETURNED_VALUE_IS_NOT.format(
                method=self.convert_response_query_graph_to_df_method,
                value='DataFrame')
        )
