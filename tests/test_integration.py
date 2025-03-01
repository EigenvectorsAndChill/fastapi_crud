"""
Simple integration test for FastAPI CRUD App using the requests library.
This avoids TestClient issues by testing against a running server.

Note: The app must be running on http://127.0.0.1:8000/ for this test to work.
Run the app with: uvicorn app.main:app --reload
"""

import unittest
import requests
import json
import warnings

# Suppress warnings
warnings.filterwarnings("ignore", category=UserWarning)
warnings.filterwarnings("ignore", category=DeprecationWarning)

# Base URL for API
BASE_URL = "http://127.0.0.1:8000"

class SimpleIntegrationTest(unittest.TestCase):
    """Simple integration test using requests library."""
    
    def setUp(self):
        """Set up for tests."""
        # Create a session for reusing connection
        self.session = requests.Session()
        
        # Store created item IDs for cleanup
        self.created_item_ids = []
    
    def tearDown(self):
        """Clean up after tests."""
        # Delete any items created during tests
        for item_id in self.created_item_ids:
            try:
                self.session.delete(f"{BASE_URL}/api/items/{item_id}")
            except:
                pass  # Ignore errors during cleanup
    
    def test_1_create_item(self):
        """Test creating a new item."""
        # Create item data
        item_data = {
            "title": "Test Item",
            "description": "This is a test item",
            "completed": False
        }
        
        # Send POST request
        response = self.session.post(
            f"{BASE_URL}/api/items/",
            json=item_data
        )
        
        # Check response
        self.assertEqual(response.status_code, 201, "Failed to create item")
        data = response.json()
        self.assertEqual(data["title"], "Test Item")
        self.assertEqual(data["description"], "This is a test item")
        self.assertEqual(data["completed"], False)
        self.assertIn("id", data)
        
        # Store ID for cleanup
        self.created_item_ids.append(data["id"])
        
        print("✅ CREATE operation works via API")
        return data["id"]  # Return ID for other tests
    
    def test_2_get_items(self):
        """Test getting all items."""
        # Create an item first
        item_id = self.test_1_create_item()
        
        # Get all items
        response = self.session.get(f"{BASE_URL}/api/items/")
        
        # Check response
        self.assertEqual(response.status_code, 200, "Failed to get items")
        data = response.json()
        self.assertIsInstance(data, list, "Response is not a list")
        self.assertGreaterEqual(len(data), 1, "No items returned")
        
        print("✅ READ operation (all items) works via API")
    
    def test_3_get_item(self):
        """Test getting a specific item."""
        # Create an item first
        item_id = self.test_1_create_item()
        
        # Get the item
        response = self.session.get(f"{BASE_URL}/api/items/{item_id}")
        
        # Check response
        self.assertEqual(response.status_code, 200, "Failed to get item")
        data = response.json()
        self.assertEqual(data["id"], item_id)
        self.assertEqual(data["title"], "Test Item")
        
        print("✅ READ operation (single item) works via API")
    
    def test_4_update_item(self):
        """Test updating an item."""
        # Create an item first
        item_id = self.test_1_create_item()
        
        # Update data
        update_data = {
            "title": "Updated Title",
            "description": "Updated description",
            "completed": True
        }
        
        # Send PUT request
        response = self.session.put(
            f"{BASE_URL}/api/items/{item_id}",
            json=update_data
        )
        
        # Check response
        self.assertEqual(response.status_code, 200, "Failed to update item")
        data = response.json()
        self.assertEqual(data["id"], item_id)
        self.assertEqual(data["title"], "Updated Title")
        self.assertEqual(data["description"], "Updated description")
        self.assertEqual(data["completed"], True)
        
        print("✅ UPDATE operation works via API")
    
    def test_5_delete_item(self):
        """Test deleting an item."""
        # Create an item first
        item_id = self.test_1_create_item()
        
        # Delete the item
        response = self.session.delete(f"{BASE_URL}/api/items/{item_id}")
        
        # Check response
        self.assertEqual(response.status_code, 204, "Failed to delete item")
        
        # Verify item is gone
        get_response = self.session.get(f"{BASE_URL}/api/items/{item_id}")
        self.assertEqual(get_response.status_code, 404, "Item still exists after deletion")
        
        # Remove from cleanup list since we already deleted it
        self.created_item_ids.remove(item_id)
        
        print("✅ DELETE operation works via API")
    
    def test_6_full_workflow(self):
        """Test a complete CRUD workflow."""
        # 1. Create
        create_data = {
            "title": "Workflow Item",
            "description": "Testing full CRUD workflow",
            "completed": False
        }
        create_response = self.session.post(f"{BASE_URL}/api/items/", json=create_data)
        self.assertEqual(create_response.status_code, 201)
        item_id = create_response.json()["id"]
        self.created_item_ids.append(item_id)
        
        # 2. Read
        read_response = self.session.get(f"{BASE_URL}/api/items/{item_id}")
        self.assertEqual(read_response.status_code, 200)
        self.assertEqual(read_response.json()["title"], "Workflow Item")
        
        # 3. Update
        update_data = {
            "title": "Updated Workflow Item",
            "description": "Updated in workflow",
            "completed": True
        }
        update_response = self.session.put(f"{BASE_URL}/api/items/{item_id}", json=update_data)
        self.assertEqual(update_response.status_code, 200)
        self.assertEqual(update_response.json()["title"], "Updated Workflow Item")
        
        # 4. Verify Update
        verify_response = self.session.get(f"{BASE_URL}/api/items/{item_id}")
        self.assertEqual(verify_response.status_code, 200)
        self.assertEqual(verify_response.json()["title"], "Updated Workflow Item")
        
        # 5. Delete
        delete_response = self.session.delete(f"{BASE_URL}/api/items/{item_id}")
        self.assertEqual(delete_response.status_code, 204)
        
        # 6. Verify Deletion
        final_response = self.session.get(f"{BASE_URL}/api/items/{item_id}")
        self.assertEqual(final_response.status_code, 404)
        
        # Remove from cleanup list
        self.created_item_ids.remove(item_id)
        
        print("✅ Full CRUD workflow works via API")

if __name__ == "__main__":
    print("\n🚀 Running simple integration tests against the API server")
    print("⚠️  Make sure the app is running with 'uvicorn app.main:app --reload'\n")
    
    try:
        unittest.main(verbosity=1)
        print("\n🎉 INTEGRATION TESTS: ALL TESTS PASSED 🎉")
    except SystemExit as e:
        if e.code != 0:
            print("\n❌ INTEGRATION TESTS: SOME TESTS FAILED ❌")