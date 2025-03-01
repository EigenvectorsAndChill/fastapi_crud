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
from app.crud.read import get_item, get_items

class TestReadOperation(unittest.TestCase):
    """Test case for the read operations."""

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
            Item(id=2, title="Item 2", description="Description 2", completed=True),
            Item(id=3, title="Item 3", description="Description 3", completed=False)
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

    def test_get_item(self):
        """Test getting a single item by ID."""
        # Get item with ID 1
        item = get_item(self.db, 1)
        
        # Check that the item was found
        self.assertIsNotNone(item)
        self.assertEqual(item.id, 1)
        self.assertEqual(item.title, "Item 1")
        self.assertEqual(item.description, "Description 1")
        self.assertEqual(item.completed, False)
        
        print("✅ test_get_item: Successfully retrieved item by ID")

    def test_get_item_not_found(self):
        """Test getting a non-existent item."""
        # Get item with ID 999 (which doesn't exist)
        item = get_item(self.db, 999)
        
        # Check that the item was not found
        self.assertIsNone(item)
        
        print("✅ test_get_item_not_found: Correctly returns None for non-existent item")

    def test_get_items(self):
        """Test getting all items."""
        # Get all items
        items = get_items(self.db)
        
        # Check that all items were returned
        self.assertEqual(len(items), 3)
        
        # Check the first item
        self.assertEqual(items[0].id, 1)
        self.assertEqual(items[0].title, "Item 1")
        
        # Check the second item
        self.assertEqual(items[1].id, 2)
        self.assertEqual(items[1].title, "Item 2")
        
        # Check the third item
        self.assertEqual(items[2].id, 3)
        self.assertEqual(items[2].title, "Item 3")
        
        print("✅ test_get_items: Successfully retrieved all items")

    def test_get_items_pagination(self):
        """Test pagination of items."""
        # Get items with skip=1 and limit=1
        items = get_items(self.db, skip=1, limit=1)
        
        # Check that only one item was returned
        self.assertEqual(len(items), 1)
        
        # Check that it's the second item
        self.assertEqual(items[0].id, 2)
        self.assertEqual(items[0].title, "Item 2")
        
        print("✅ test_get_items_pagination: Pagination works correctly")

if __name__ == "__main__":
    try:
        unittest.main(verbosity=0)
        print("\n🎉 READ OPERATION: ALL TESTS PASSED 🎉")
    except SystemExit as e:
        if e.code != 0:
            print("\n❌ READ OPERATION: TESTS FAILED ❌")
            sys.exit(1)