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

import networkx as nx
import scipy as sp
from django.core.management.base import BaseCommand

from graph.models import Entity


class Command(BaseCommand):
    help = 'incidence matrix'

    def handle(self, *args, **kwargs):

        # select graph
        my_graph = Entity.objects.get(label='Test Graph 3')
        # fetch graph data
        nx_graph = my_graph.get_networkx_graph()

        # create node / edge lists
        nodelist = list(nx_graph)
        node_index = {node: i for i, node in enumerate(nodelist)}
        edgelist = list(nx_graph.edges(keys=True, data=True))

        for u, v, k, d in nx_graph.edges(keys=True, data=True):
            print(u, "->", v, "label =", k, "weight =", d['weight'])

        # determine vector size of weights
        vector_size = len(edgelist[0][3]['weight'])

        # initialize incidence tensor (list of Scipy sparse matrices, one per dimension)

        incidence_tensor = []

        for d in range(vector_size):
            a = sp.sparse.lil_array((len(nodelist), len(edgelist)))
            for ei, e in enumerate(edgelist):
                (u, v) = e[:2]  # isolate the node data
                if u == v:
                    continue  # self loops give zero column
                try:
                    ui = node_index[u]  # get indices of nodes
                    vi = node_index[v]
                except KeyError as err:
                    raise nx.NetworkXError(
                        f"node {u} or {v} in edgelist but not in nodelist"
                    ) from err

                ekey = e[2]  # fetch the edge key (label)
                wt_vector = nx_graph[u][v][ekey].get('weight', 1)
                a[ui, ei] = -wt_vector[d]
                a[vi, ei] = wt_vector[d]
            incidence_tensor.append(a)

        for d in range(vector_size):
            print(80 * '-')
            print(incidence_tensor[d].todense())
