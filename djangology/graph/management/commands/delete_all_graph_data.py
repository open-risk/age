# Copyright (c) 2025 - 2026 Open Risk (https://www.openriskmanagement.com)
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

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
