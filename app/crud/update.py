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
    # TODO: Implement the update_item function
    # The function should:
    # 1. Get the item with the given item_id from the database
    # 2. If the item doesn't exist, return None
    # 3. Update the item's attributes with the new values
    # 4. Commit the changes to the database
    # 5. Refresh the item from the database
    # 6. Return the updated item
    
    # Delete the code below and implement your solution
    raise NotImplementedError("The update_item function is not implemented yet")