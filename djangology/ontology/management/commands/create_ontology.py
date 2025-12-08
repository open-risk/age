from django.core.management.base import BaseCommand
from owlready2 import *


class Command(BaseCommand):
    help = 'create a DEB accounting ontology'

    def handle(self, *args, **kwargs):

        # Create a new root ontology of accounts
        onto = get_ontology("http://www.openriskmanual.org/ns/account_ontology.owl")
        onto_classes = get_ontology("http://www.openriskmanual.org/ns/accounts.owl")
        onto_classes.imported_ontologies.append(onto)

        stocks = ['Asset', 'Liability', 'Equity', 'Inventory', 'Cash', 'Cash Equivalent', 'Trade Receivable',
                  'Share Capital', 'Retained Earnings', 'Other Equity', 'Borrowing', 'Provision', 'Lease', 'Pension',
                  'Deferred Tax', 'Income Tax', 'Property', 'Plant', 'Equipment', 'Goodwill']
        flows = ['Revenue', 'Other Income', 'Expense', 'Loss', 'Cost of Sales', 'Depreciation']
        modifiers = ['Current', 'Non-current', 'Intangible', 'Investment', 'Financing', 'Operating']

        with onto:
            for entity in stocks:
                Class = types.new_class(entity, (Thing,))
            for entity in flows:
                Class = types.new_class(entity, (Thing,))
            for entity in modifiers:
                Class = types.new_class(entity, (Thing,))

        # Save the ontology to a file
        onto.save(file="account_ontology.owl", format="rdfxml")
