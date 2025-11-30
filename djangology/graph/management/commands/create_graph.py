import networkx as nx
from django.core.management.base import BaseCommand, CommandError

class Command(BaseCommand):
    help = 'create graph'

    def handle(self, *args, **kwargs):

        MD = nx.MultiDiGraph()
        MD.add_edge('A', 'B', relation='monetary', weight=10)
        MD.add_edge('A', 'B', relation='energy', weight=22)
        MD.add_edge('A', 'B', relation='embodied', weight=12)

        for u, v, k, d in MD.edges(keys=True, data=True):
            print(u, "->", v, "key=", k, "data=", d)

        print("Edges A->B:", list(MD.get_edge_data('A', 'B').items()))

        # iterate over nodes
        # create and save nodes
        # iterate over edges
        # create and save edges