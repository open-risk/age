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

from django.core.management.base import BaseCommand
from taggit.models import Tag


class Command(BaseCommand):
    help = 'create a predefined list of account tags'

    def handle(self, *args, **kwargs):
        stocks = ['Asset', 'Liability', 'Equity', 'Inventory', 'Cash', 'Cash Equivalent', 'Trade Receivable',
                  'Share Capital', 'Retained Earnings', 'Other Equity', 'Borrowing', 'Provision', 'Lease', 'Pension',
                  'Deferred Tax', 'Income Tax', 'Property', 'Plant', 'Equipment', 'Goodwill']
        flows = ['Revenue', 'Other Income', 'Expense', 'Loss', 'Cost of Sales', 'Depreciation']
        modifiers = ['Current', 'Non-current', 'Intangible', 'Investment', 'Financing', 'Operating']

        predefined_tags = stocks + flows + modifiers

        # Create predefined tags (if they do not exist)
        for tag_name in predefined_tags:
            Tag.objects.get_or_create(name=tag_name)
