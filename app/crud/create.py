from sqlalchemy.orm import Session
from app.models.item import Item
from app.schemas.item import ItemCreate

def create_item(db: Session, item: ItemCreate):
    db_item = Item(title=item.title,description=item.description,completed=item.completed)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item
    """
    Create a new item in the database.
    
    Args:
        db (Session): Database session
        item (ItemCreate): Item data to create
        
    Returns:
        Item: The created item
    """
    # TODO: Implement the create_item function
    # The function should:
    # 1. Create a new Item object with the data from item
    # 2. Add the item to the database session
    # 3. Commit the transaction
    # 4. Refresh the item to get the generated ID
    # 5. Return the created item
    
   