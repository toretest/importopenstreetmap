# python
from typing import Dict, Any


def create_or_update_customer(customer_id: str, data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Create a new customer or update an existing one.

    Args:
        customer_id: The unique identifier of the customer.
        data: A dictionary with customer fields, e.g. {"name": "...", "email": "..."}

    Returns:
        A dictionary representing the created/updated customer.
    """
    # In a real implementation, you might:
    # - Look up the customer in a database
    # - Create or update the record
    # - Return the saved record
    # Below is a simple example implementation:
    is_update = bool(customer_id)
    result = {
        "id": customer_id or "<generated-id>",
        "name": data.get("name", "<name>"),
        "email": data.get("email", "<email@example.com>"),
        "status": "updated" if is_update else "created",
    }
    print(f"Customer {result['status']}: {result['id']} -> {result['name']} ({result['email']})")
    return result