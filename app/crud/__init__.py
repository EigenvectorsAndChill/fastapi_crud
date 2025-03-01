"""
CRUD operations for the Item model.
This module imports and exposes all CRUD operations from their respective modules.
"""

# Import operations
from app.crud.create import create_item
from app.crud.read import get_item, get_items
from app.crud.update import update_item
from app.crud.delete import delete_item

# Re-export all operations
__all__ = [
    "create_item",  # Create operations
    "get_item", "get_items",  # Read operations
    "update_item",  # Update operations
    "delete_item",  # Delete operations
]