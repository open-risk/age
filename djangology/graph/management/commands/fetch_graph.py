from django.core.management.base import BaseCommand

from graph.models import Entity


class Command(BaseCommand):
    help = 'fetch nx graph from storage'

    def handle(self, *args, **kwargs):
        my_graph = Entity.objects.get(identity='Company 1 Graph')
        nx_graph = my_graph.get_networkx_graph()

        for u, data in nx_graph.nodes(data=True):
            print(u, "->", "tags =", data["tags"])

        for u, v, key, data in nx_graph.edges(keys=True, data=True):
            print(u, "->", v, "key =", key, "weight =", data['weight'], "tags =", data["tags"])
