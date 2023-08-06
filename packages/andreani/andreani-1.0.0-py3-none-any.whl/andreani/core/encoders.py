import json
from decimal import Decimal


class DecimalEncoder(json.JSONEncoder):
    """See https://bobbyhadz.com/blog/python-typeerror-object-of-type-decimal-is-not-json-serializable"""

    def default(self, obj):
        # 👇️ if passed in object is instance of Decimal
        # convert it to a string
        if isinstance(obj, Decimal):
            return float(obj)
        # 👇️ otherwise use the default behavior
        return json.JSONEncoder.default(self, obj)
