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
    # Query the database for an item with the specified ID
    # Using filter and first() to return None if not found
    return db.query(Item).filter(Item.id == item_id).first()

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
    # Query all items with pagination
    # offset - how many records to skip
    # limit - maximum number of records to return
    return db.query(Item).offset(skip).limit(limit).all()