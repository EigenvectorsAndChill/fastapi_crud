from sqlalchemy.orm import Session
from typing import Dict, Any, Optional
from app.models.item import Item
from app.schemas.item import ItemCreate

def update_item(db: Session, item_id: int, item: ItemCreate) -> Optional[Item]:
    """
    Update an existing item in the database.
    
    Args:
        db (Session): Database session
        item_id (int): ID of the item to update
        item (ItemCreate): New item data
        
    Returns:
        Optional[Item]: The updated item or None if not found
    """
    # First retrieve the item to update
    db_item = db.query(Item).filter(Item.id == item_id).first()
    
    # If the item doesn't exist, return None
    if db_item is None:
        return None
    
    # Update the item's attributes with the new values
    # Using model_dump instead of dict for Pydantic v2 compatibility
    item_data = item.model_dump(exclude_unset=True)
    for key, value in item_data.items():
        setattr(db_item, key, value)
    
    # Commit the changes to the database
    db.commit()
    
    # Refresh the item to ensure it reflects the current state in the database
    db.refresh(db_item)
    
    # Return the updated item
    return db_item