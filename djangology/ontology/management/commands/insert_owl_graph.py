from django.core.management.base import BaseCommand, CommandError
from owlready2 import get_ontology, Thing, World


class Command(BaseCommand):
    help = 'insert graph from file'

    def add_arguments(self, parser):
        parser.add_argument('file_path', type=str, help='The file path to the graph')

    def handle(self, *args, **kwargs):

        my_world = World(filename="./db.sqlite3", exclusive=False)
        file_path = kwargs['file_path']
        onto = my_world.get_ontology(file_path).load()
        print(onto.world)
        print(onto.base_iri)
        print(list(onto.classes()))

        with onto:
            class Account(Thing):
                pass

        print(Account.iri)
        my_world.save()

        self.stdout.write(self.style.SUCCESS('Successfully inserted graph'))
