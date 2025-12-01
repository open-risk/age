from django.core.management.base import BaseCommand

from graph.models import Entity


class Command(BaseCommand):
    help = 'fetch nx graph from storage'

    def handle(self, *args, **kwargs):
        my_graph = Entity.objects.get(label='Test Graph')
        nx_graph = my_graph.get_networkx_graph()

        for u, v, k, d in nx_graph.edges(keys=True, data=True):
            print(u, "->", v, "label =", d['label'], "weight =", d['weight'])
