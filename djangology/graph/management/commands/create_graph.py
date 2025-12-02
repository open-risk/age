import networkx as nx
import numpy as np
from django.core.management.base import BaseCommand, CommandError
from graph.models import Entity


class Command(BaseCommand):
    help = 'create and store nx graph'

    def handle(self, *args, **kwargs):
        nx_graph = nx.MultiDiGraph(label='Test Graph 4')
        nx_graph.add_node('A')
        nx_graph.add_node('B')
        nx_graph.add_node('C')
        nx_graph.add_edge('A', 'B', key='T1', weight=np.array([1.0, 0.5, 0.2]))
        nx_graph.add_edge('B', 'C', key='T2', weight=np.array([2.0, 1.5, 0.8]))

        for u, v, k, d in nx_graph.edges(keys=True, data=True):
            print(u, "->", v, "label =", k, "weight =", d['weight'])

        my_graph = Entity(label=nx_graph.graph['label'])
        my_graph.save()
        my_graph.store_networkx_graph(nx_graph)
