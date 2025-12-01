import networkx as nx
import numpy as np
from django.core.management.base import BaseCommand, CommandError
from graph.models import Entity


class Command(BaseCommand):
    help = 'create and store nx graph'

    def handle(self, *args, **kwargs):
        nx_graph = nx.MultiDiGraph(label='Test Graph 3')
        nx_graph.add_node('A')
        nx_graph.add_node('B')
        nx_graph.add_edge('A', 'B', label='T1', weight=np.array([1.0, 0.5, 0.2]))

        for u, v, k, d in nx_graph.edges(keys=True, data=True):
            print(u, "->", v, "label =", d['label'], "weight =", d['weight'])

        print("Edges A->B:", list(nx_graph.get_edge_data('A', 'B').items()))

        my_graph = Entity(label=nx_graph.graph['label'])
        my_graph.save()
        my_graph.store_networkx_graph(nx_graph)
