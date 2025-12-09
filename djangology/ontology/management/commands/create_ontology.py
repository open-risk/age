from django.core.management.base import BaseCommand
from owlready2 import *


class Command(BaseCommand):
    help = 'create a DEB accounting ontology'

    def handle(self, *args, **kwargs):

        # Create a new root ontology of accounts
        onto = get_ontology("http://www.openriskmanual.org/ns/account_ontology.owl")
        onto_classes = get_ontology("http://www.openriskmanual.org/ns/accounts.owl")
        onto_classes.imported_ontologies.append(onto)

        # This is the highest level categorization. It defines which accounts appear in balance sheet type reports
        # versus profit and loss reports

        dynamic_type = ['Stock', 'Flow']

        # Categorisation of stock type accounts (TODO split into subclasses)
        stocks = ['Asset', 'Liability', 'Equity', 'Inventory', 'Cash', 'Cash_Equivalent', 'Trade_Receivable',
                  'Share_Capital', 'Retained_Earnings', 'Other_Equity', 'Borrowing', 'Provision', 'Lease', 'Pension',
                  'Deferred_Tax', 'Income_Tax', 'Property', 'Plant', 'Equipment', 'Goodwill']

        # Attributes that may apply to some stock accounts
        stock_modifiers = ['Current', 'Non-current', 'Intangible']

        # Categorization of flow type accounts
        flows = ['Revenue', 'Other_Income', 'Expense', 'Loss', 'Cost_Of_Sales', 'Depreciation']

        # Attributes that may apply to some flow accounts (in particular for IFRS 18 purposes)
        flow_modifiers = ['Investment', 'Financing', 'Operating']

        with onto:
            for entity in dynamic_type:
                Class = types.new_class(entity, (Thing,))
            for entity in stocks:
                Class = types.new_class(entity, (onto.Stock,))
            for entity in flows:
                Class = types.new_class(entity, (onto.Flow,))
            for entity in stock_modifiers:
                Class = types.new_class(entity, (onto.Stock,))
            for entity in flow_modifiers:
                Class = types.new_class(entity, (onto.Flow,))

        # Save the ontology to a file
        onto.save(file="account_ontology.owl", format="rdfxml")
