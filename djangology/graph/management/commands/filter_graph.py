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
from django.core.management.base import BaseCommand

from graph.models import Entity


class Command(BaseCommand):
    help = 'filter graph to find similarly tagged transactions'

    def handle(self, *args, **kwargs):

        # Fetch the entire accounting graph
        my_graph = Entity.objects.get(identity='Company 1 Graph')
        nx_graph = my_graph.get_networkx_graph()
        for u, data in nx_graph.nodes(data=True):
            print(u, "->", "tags =", data["tags"])

        for u, v, key, data in nx_graph.edges(keys=True, data=True):
            print(u, "->", v, "key =", key, "weight =", data['weight'], "tags =", data["tags"])

        # Define the tags we want to filter by
        # account_tags = {'todo'}
        transaction_tags = {'Transfer'}

        # Create an empty subgraph
        H = nx.MultiDiGraph()

        # Add filtered transactions, and the corresponding accounts
        for u, v, data in nx_graph.edges(data=True):
            for tag in data['tags']:
                if tag in transaction_tags:
                    if u not in H:
                        H.add_node(u, tags=nx_graph.nodes[u]['tags'])
                    if v not in H:
                        H.add_node(v, tags=nx_graph.nodes[v]['tags'])
                    H.add_edge(u, v, **data)

        for u, data in H.nodes(data=True):
            print(u, "->", "tags =", data["tags"])

        for u, v, key, data in H.edges(keys=True, data=True):
            print(u, "->", v, "key =", key, "weight =", data['weight'], "tags =", data["tags"])
