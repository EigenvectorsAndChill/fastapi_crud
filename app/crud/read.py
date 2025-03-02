from sqlalchemy.orm import Session
from typing import List, Optional
from app.models.item import Item

def get_item(db: Session, item_id: int) -> Optional[Item]:
    item = db.query(Item).filter(Item.id == item_id).first()
    return item

def get_items(db: Session, skip: int = 0, limit: int = 100) -> List[Item]:
    item_list = db.query(Item).offset(skip).limit(limit).all()
    return item_list