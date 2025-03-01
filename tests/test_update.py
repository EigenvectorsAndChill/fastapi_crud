import unittest
import sys
import os
import warnings
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Suppress warnings
warnings.filterwarnings("ignore", category=UserWarning)
warnings.filterwarnings("ignore", category=DeprecationWarning)

# Add the parent directory to the sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.database import Base
from app.models.item import Item
from app.schemas.item import ItemCreate
from app.crud.update import update_item

class TestUpdateOperation(unittest.TestCase):
    """Test case for the update operation."""

    def setUp(self):
        """Set up a new test database for each test."""
        # Create an in-memory SQLite database for testing
        self.engine = create_engine("sqlite:///:memory:")
        
        # Create the tables
        Base.metadata.create_all(self.engine)
        
        # Create a session
        TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)
        self.db = TestingSessionLocal()
        
        # Add test data
        self.test_item = Item(id=1, title="Original Title", description="Original Description", completed=False)
        self.db.add(self.test_item)
        self.db.commit()

    def tearDown(self):
        """Clean up after each test."""
        # Drop all tables
        Base.metadata.drop_all(self.engine)
        
        # Close the session
        self.db.close()

    def test_update_item(self):
        """Test updating an existing item."""
        # Create new data for the item
        updated_data = ItemCreate(
            title="Updated Title",
            description="Updated Description",
            completed=True
        )
        
        # Update the item
        updated_item = update_item(self.db, 1, updated_data)
        
        # Check that the item was updated
        self.assertIsNotNone(updated_item)
        self.assertEqual(updated_item.id, 1)
        self.assertEqual(updated_item.title, "Updated Title")
        self.assertEqual(updated_item.description, "Updated Description")
        self.assertEqual(updated_item.completed, True)
        
        # Check that the item was updated in the database
        db_item = self.db.query(Item).filter(Item.id == 1).first()
        self.assertEqual(db_item.title, "Updated Title")
        self.assertEqual(db_item.description, "Updated Description")
        self.assertEqual(db_item.completed, True)
        
        print("✅ test_update_item: Item was updated successfully")

    def test_update_item_partial(self):
        """Test updating only some fields of an item."""
        # Create new data with only title changed
        updated_data = ItemCreate(
            title="Updated Title Only",
            description="Original Description",
            completed=False
        )
        
        # Update the item
        updated_item = update_item(self.db, 1, updated_data)
        
        # Check that only the title was updated
        self.assertEqual(updated_item.id, 1)
        self.assertEqual(updated_item.title, "Updated Title Only")
        self.assertEqual(updated_item.description, "Original Description")
        self.assertEqual(updated_item.completed, False)
        
        print("✅ test_update_item_partial: Partial update works correctly")

    def test_update_item_not_found(self):
        """Test updating a non-existent item."""
        # Create new data
        updated_data = ItemCreate(
            title="Updated Title",
            description="Updated Description",
            completed=True
        )
        
        # Try to update a non-existent item
        updated_item = update_item(self.db, 999, updated_data)
        
        # Check that None was returned
        self.assertIsNone(updated_item)
        
        print("✅ test_update_item_not_found: Correctly returns None for non-existent item")

if __name__ == "__main__":
    try:
        unittest.main(verbosity=0)
        print("\n🎉 UPDATE OPERATION: ALL TESTS PASSED 🎉")
    except SystemExit as e:
        if e.code != 0:
            print("\n❌ UPDATE OPERATION: TESTS FAILED ❌")
            sys.exit(1)