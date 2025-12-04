import networkx as nx
from django.core.management.base import BaseCommand
import networkx as nx
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
