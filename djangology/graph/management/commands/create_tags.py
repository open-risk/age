from django.core.management.base import BaseCommand
from taggit.models import Tag


class Command(BaseCommand):
    help = 'create a predefined list of account tags'

    def handle(self, *args, **kwargs):

        stocks = ['Asset', 'Liability', 'Equity', 'Inventory', 'Cash', 'Cash Equivalent', 'Trade Receivable', 'Share Capital', 'Retained Earnings', 'Other Equity', 'Borrowing', 'Provision', 'Lease', 'Pension', 'Deferred Tax', 'Income Tax', 'Property', 'Plant', 'Equipment', 'Goodwill']
        flows = ['Revenue', 'Other Income', 'Expense', 'Loss', 'Cost of Sales', 'Depreciation']
        modifiers = ['Current', 'Non-current', 'Intangible', 'Investment', 'Financing', 'Operating']

        predefined_tags = stocks + flows + modifiers

        # Create predefined tags (if they do not exist)
        for tag_name in predefined_tags:
            Tag.objects.get_or_create(name=tag_name)
