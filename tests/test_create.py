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
from app.crud.create import create_item

class TestCreateOperation(unittest.TestCase):
    """Test case for the create operation."""

    def setUp(self):
        """Set up a new test database for each test."""
        # Create an in-memory SQLite database for testing
        self.engine = create_engine("sqlite:///:memory:")
        
        # Create the tables
        Base.metadata.create_all(self.engine)
        
        # Create a session
        TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)
        self.db = TestingSessionLocal()

    def tearDown(self):
        """Clean up after each test."""
        # Drop all tables
        Base.metadata.drop_all(self.engine)
        
        # Close the session
        self.db.close()

    def test_create_item(self):
        """Test creating a new item."""
        # Create a new item
        item_data = ItemCreate(
            title="Test Item",
            description="This is a test item",
            completed=False
        )
        
        # Call the create_item function
        item = create_item(self.db, item_data)
        
        # Check that the item was created and has an ID
        self.assertIsNotNone(item)
        self.assertIsNotNone(item.id)
        
        # Check that the item has the correct data
        self.assertEqual(item.title, "Test Item")
        self.assertEqual(item.description, "This is a test item")
        self.assertEqual(item.completed, False)
        
        # Check that the item exists in the database
        db_item = self.db.query(Item).filter(Item.id == item.id).first()
        self.assertIsNotNone(db_item)
        self.assertEqual(db_item.title, "Test Item")
        
        print("✅ test_create_item: Item creation works correctly")

    def test_create_item_no_description(self):
        """Test creating a new item without a description."""
        # Create a new item
        item_data = ItemCreate(
            title="Test Item No Description",
            completed=True
        )
        
        # Call the create_item function
        item = create_item(self.db, item_data)
        
        # Check that the item was created and has an ID
        self.assertIsNotNone(item)
        self.assertIsNotNone(item.id)
        
        # Check that the item has the correct data
        self.assertEqual(item.title, "Test Item No Description")
        self.assertIsNone(item.description)
        self.assertEqual(item.completed, True)
        
        print("✅ test_create_item_no_description: Item creation without description works correctly")

if __name__ == "__main__":
    try:
        unittest.main(verbosity=0)
        print("\n🎉 CREATE OPERATION: ALL TESTS PASSED 🎉")
    except SystemExit as e:
        if e.code != 0:
            print("\n❌ CREATE OPERATION: TESTS FAILED ❌")
            sys.exit(1)