from django.core.management.base import BaseCommand, CommandError

from graph.models import Entity, Transaction, Account


class Command(BaseCommand):
    help = 'Deletes all graph data from the database'

    Transaction.objects.all().delete()
    Account.objects.all().delete()
    Entity.objects.all().delete()

    def handle(self, *args, **options):
        self.stdout.write(
            self.style.WARNING(f"WARNING: This will delete all graph data and metadata.")
        )

        self.stdout.write(self.style.WARNING("This action cannot be undone!"))
        confirmation = input("Type 'yes' to confirm: ").strip().lower()

        if confirmation != "yes":
            raise CommandError("Aborted: You did not confirm deletion of all graph data.")

        self.stdout.write(self.style.SUCCESS('Successfully deleted all graph data and metadata'))
