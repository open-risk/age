# Copyright (c) 2025 - 2026 Open Risk (https://www.openriskmanagement.com)
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

from django.test import TestCase
import networkx as nx
import numpy as np
from graph.models import Entity, Account, Transaction


class ManagerModelTests(TestCase):

    def setUp(self):
        self.graph = Entity.objects.create(label="Test Graph")
        self.node1 = Account.objects.create(label="A", graph=self.graph)
        self.node2 = Account.objects.create(label="B", graph=self.graph)
        self.edge = Transaction.objects.create(label="T1", graph=self.graph, source=self.node1, target=self.node2, )

    def test_graph_roundtrip(self):
        # step 1
        test_graph = nx.MultiDiGraph(label='Test Graph X')  # empty graph
        test_graph.add_node('A1')
        test_graph.add_node('B1')
        test_graph.add_edge('A1', 'B1', key='TX', weight=np.array([1.0, 0.5, 0.2]))

        for node, data in test_graph.nodes(data=True):
            print(node, data)
        for u, v, k, d in test_graph.edges(keys=True, data=True):
            print(u, "->", v, "label =", k, "weight =", d['weight'])

        # step 2

        input_graph = Entity(label=test_graph.graph['label'])
        input_graph.save()
        input_graph.store_networkx_graph(test_graph)

        # step 3

        output_graph = Entity.objects.get(label='Test Graph X')
        stored_graph = output_graph.get_networkx_graph()

        for node, data in stored_graph.nodes(data=True):
            print(node, data)
        for u, v, k, d in stored_graph.edges(keys=True, data=True):
            print(u, "->", v, "label =", k, "weight =", d['weight'])
        self.assertEqual(True, nx.is_isomorphic(test_graph, stored_graph))

        # Does not work for vector weights
        # self.assertEqual(True, nx.utils.graphs_equal(test_graph, stored_graph))
