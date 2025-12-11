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
