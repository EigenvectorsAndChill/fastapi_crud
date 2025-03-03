from sqlalchemy.orm import Session
from app.models.item import Item
from app.schemas.item import ItemCreate

def create_item(db: Session, item: ItemCreate):
    """
    Create a new item in the database.
    
    Args:
        db (Session): Database session
        item (ItemCreate): Item data to create
        
    Returns:
        Item: The created item
    """
    # Create a new item object with the provided data
    db_item = Item(
        title=item.title,
        description=item.description,
        completed=item.completed
    )
    
    # Add the item to the database session
    db.add(db_item)
    
    # Commit the transaction to save the item
    db.commit()
    
    # Refresh the item to get the generated ID and other default values
    db.refresh(db_item)
    
    # Return the created item
    return db_item