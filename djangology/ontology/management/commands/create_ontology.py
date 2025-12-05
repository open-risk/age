from django.core.management.base import BaseCommand
from owlready2 import *


class Command(BaseCommand):
    help = 'create a deb ontology'

    def handle(self, *args, **kwargs):
        stocks = ['Asset', 'Liability', 'Equity', 'Inventory', 'Cash', 'Cash Equivalent', 'Trade Receivable',
                  'Share Capital', 'Retained Earnings', 'Other Equity', 'Borrowing', 'Provision', 'Lease', 'Pension',
                  'Deferred Tax', 'Income Tax', 'Property', 'Plant', 'Equipment', 'Goodwill']
        flows = ['Revenue', 'Other Income', 'Expense', 'Loss', 'Cost of Sales', 'Depreciation']
        modifiers = ['Current', 'Non-current', 'Intangible', 'Investment', 'Financing', 'Operating']

        # Create a new ontology
        onto = get_ontology("http://www.openriskmanual.org/ns/account_ontology.owl")

        # Define a class
        with onto:
            class Account(Thing):
                pass

        # Save the ontology to a file
        onto.save(file="account_ontology.owl", format="rdfxml")
