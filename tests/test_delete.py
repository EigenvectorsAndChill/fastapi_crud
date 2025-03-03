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
from app.crud.delete import delete_item

class TestDeleteOperation(unittest.TestCase):
    """Test case for the delete operation."""

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
        self.test_items = [
            Item(id=1, title="Item 1", description="Description 1", completed=False),
            Item(id=2, title="Item 2", description="Description 2", completed=True)
        ]
        
        for item in self.test_items:
            self.db.add(item)
        
        self.db.commit()

    def tearDown(self):
        """Clean up after each test."""
        # Drop all tables
        Base.metadata.drop_all(self.engine)
        
        # Close the session
        self.db.close()

    def test_delete_item(self):
        """Test deleting an existing item."""
        # Delete item with ID 1
        result = delete_item(self.db, 1)
        
        # Check that the deletion was successful
        self.assertTrue(result)
        
        # Check that the item no longer exists in the database
        item = self.db.query(Item).filter(Item.id == 1).first()
        self.assertIsNone(item)
        
        # Check that the other item still exists
        remaining_item = self.db.query(Item).filter(Item.id == 2).first()
        self.assertIsNotNone(remaining_item)
        
        print("✅ test_delete_item: Item was deleted successfully")

    def test_delete_item_not_found(self):
        """Test deleting a non-existent item."""
        # Try to delete an item with ID 999 (which doesn't exist)
        result = delete_item(self.db, 999)
        
        # Check that the deletion failed (returned False)
        self.assertFalse(result)
        
        # Check that both original items still exist
        count = self.db.query(Item).count()
        self.assertEqual(count, 2)
        
        print("✅ test_delete_item_not_found: Correctly returns False for non-existent item")

if __name__ == "__main__":
    try:
        unittest.main(verbosity=0)
        print("\n🎉 DELETE OPERATION: ALL TESTS PASSED 🎉")
    except SystemExit as e:
        if e.code != 0:
            print("\n❌ DELETE OPERATION: TESTS FAILED ❌")
            sys.exit(1)
