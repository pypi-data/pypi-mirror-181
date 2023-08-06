"""
Tasks for interacting with Zoho Inventory.
"""
try:
    from .tasks.contacts import Create, List, Fetch, Update, Delete, ListComments, ListContactPersons, MarkAsActive, \
        MarkAsInactive, GetEmailStatement, SendEmailStatement, SendEmail
    from .tasks.contact_persons import Create, List, Fetch, Update, Delete, MarkAsPrimary
    from .tasks.items import Create, List, Fetch, Update, Delete, MarkAsActive, MarkAsInactive, FetchPriceBookRate
    from .tasks.sales_orders import Create, List, Fetch, Update, Delete, MarkAsVoid, MarkAsConfirmed
    from .tasks.shipment_orders import Create, Fetch, Delete, MarkAsDelivered
except ImportError:
    raise ImportError(
        'Using `prefect.tasks.zoho_inventory` requires Prefect to be installed with the "zoho-inventory-python-sdk" '
        'extra. '
    )

from ._version import get_versions

__version__ = get_versions()['version']
del get_versions
