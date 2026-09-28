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
import numpy as np
from django.core.management.base import BaseCommand

from graph.models import Entity


class Command(BaseCommand):
    help = 'create and store nx graph'

    def handle(self, *args, **kwargs):
        # Account Graph
        nx_graph = nx.MultiDiGraph(identity='Company 1 Graph')

        # Accounts (Nodes)
        nx_graph.add_node('A', tag='Asset')
        nx_graph.add_node('B', tag='Liability')
        nx_graph.add_node('C', tag='Liability')

        # Transactions (Edges)
        nx_graph.add_edge('A', 'B', key='T01', tag='Transfer', weight=np.array([1.0, 0.5, 0.2]))
        nx_graph.add_edge('A', 'B', key='T02', tag='Transfer', weight=np.array([0.0, 1.5, 3.2]))
        nx_graph.add_edge('B', 'C', key='T03', tag='Purchase', weight=np.array([2.0, 1.5, 0.8]))

        for u, v, k, d in nx_graph.edges(keys=True, data=True):
            print(u, "->", v, "key =", k, "weight =", d['weight'], "tag =", d['tag'])

        # Persist Accounting Graph as Django/Sqlite objects

        my_graph = Entity(identity=nx_graph.graph['identity'])
        my_graph.save()
        my_graph.store_networkx_graph(nx_graph)
