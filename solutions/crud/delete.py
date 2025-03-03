from sqlalchemy.orm import Session
from typing import Optional
from app.models.item import Item

def delete_item(db: Session, item_id: int) -> bool:
    """
    Delete an item from the database.
    
    Args:
        db (Session): Database session
        item_id (int): ID of the item to delete
        
    Returns:
        bool: True if the item was deleted, False if the item was not found
    """
    # First retrieve the item to delete
    db_item = db.query(Item).filter(Item.id == item_id).first()
    
    # If the item doesn't exist, return False
    if db_item is None:
        return False
    
    # Delete the item from the database
    db.delete(db_item)
    
    # Commit the changes to the database
    db.commit()
    
    # Return True to indicate successful deletion
    return True