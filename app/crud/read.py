from sqlalchemy.orm import Session
from typing import List, Optional
from app.models.item import Item

def get_item(db: Session, item_id: int) -> Optional[Item]:
    """
    Get a single item by ID.
    
    Args:
        db (Session): Database session
        item_id (int): ID of the item to retrieve
        
    Returns:
        Optional[Item]: The found item or None if not found
    """
    # TODO: Implement the get_item function
    # The function should:
    # 1. Query the database for an item with the given item_id
    # 2. Return the item if found, None otherwise
    
    # Delete the code below and implement your solution
    raise NotImplementedError("The get_item function is not implemented yet")

def get_items(db: Session, skip: int = 0, limit: int = 100) -> List[Item]:
    """
    Get multiple items with pagination.
    
    Args:
        db (Session): Database session
        skip (int): Number of records to skip (for pagination)
        limit (int): Maximum number of records to return
        
    Returns:
        List[Item]: List of found items
    """
    # TODO: Implement the get_items function
    # The function should:
    # 1. Query the database for all items
    # 2. Apply pagination using skip and limit parameters
    # 3. Return the list of items
    
    # Delete the code below and implement your solution
    raise NotImplementedError("The get_items function is not implemented yet")