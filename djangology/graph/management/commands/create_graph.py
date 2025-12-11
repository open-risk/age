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
