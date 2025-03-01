// DOM Elements
const itemForm = document.getElementById('item-form');
const formTitle = document.getElementById('form-title');
const itemIdInput = document.getElementById('item-id');
const titleInput = document.getElementById('title');
const descriptionInput = document.getElementById('description');
const completedCheckbox = document.getElementById('completed');
const submitBtn = document.getElementById('submit-btn');
const cancelBtn = document.getElementById('cancel-btn');
const itemsTableBody = document.getElementById('items-table-body');
const noItemsMessage = document.getElementById('no-items-message');
const createFirstItemBtn = document.getElementById('create-first-item-btn');
const loadingSpinner = document.getElementById('loading-spinner');
const toastElement = document.getElementById('toast');
const toastTitle = document.getElementById('toast-title');
const toastMessage = document.getElementById('toast-message');
const toastIcon = document.getElementById('toast-icon');

// Create Bootstrap toast instance
const toast = new bootstrap.Toast(toastElement, {
    delay: 3000
});

// API Endpoints
const API_URL = '/api/items';

// App State
let isEditing = false;
let items = [];

// Event Listeners
document.addEventListener('DOMContentLoaded', fetchItems);
itemForm.addEventListener('submit', handleFormSubmit);
cancelBtn.addEventListener('click', resetForm);
if (createFirstItemBtn) {
    createFirstItemBtn.addEventListener('click', () => {
        window.scrollTo({
            top: itemForm.offsetTop - 100,
            behavior: 'smooth'
        });
        titleInput.focus();
    });
}

// Functions
async function fetchItems() {
    try {
        showLoading(true);
        const response = await fetch(API_URL);
        const data = await response.json();
        
        // Keep a reference to all items
        items = data;
        
        renderItems(items);
        showLoading(false);
    } catch (error) {
        console.error('Error fetching items:', error);
        showToast('Error', 'Failed to load items. Please try again.', 'error');
        showLoading(false);
    }
}

function renderItems(items) {
    itemsTableBody.innerHTML = '';
    
    if (items.length === 0) {
        noItemsMessage.style.display = 'block';
        document.querySelector('.table-responsive').style.display = 'none';
        return;
    }
    
    noItemsMessage.style.display = 'none';
    document.querySelector('.table-responsive').style.display = 'block';
    
    items.forEach(item => {
        const row = document.createElement('tr');
        row.id = `item-row-${item.id}`;
        
        row.innerHTML = `
            <td>${item.id}</td>
            <td class="fw-medium">${escapeHtml(item.title)}</td>
            <td>${escapeHtml(item.description || '-')}</td>
            <td>
                <span class="badge completed-${item.completed}">
                    ${item.completed ? 
                      '<i class="bi bi-check-circle me-1"></i>Completed' : 
                      '<i class="bi bi-clock me-1"></i>Pending'}
                </span>
            </td>
            <td class="text-center">
                <div class="d-flex justify-content-center">
                    <button class="action-btn edit-btn" data-id="${item.id}" title="Edit Item">
                        <i class="bi bi-pencil-square"></i>
                    </button>
                    <button class="action-btn delete-btn" data-id="${item.id}" title="Delete Item">
                        <i class="bi bi-trash"></i>
                    </button>
                </div>
            </td>
        `;
        
        itemsTableBody.appendChild(row);
        
        // Add event listeners to buttons
        const editBtn = row.querySelector('.edit-btn');
        const deleteBtn = row.querySelector('.delete-btn');
        
        editBtn.addEventListener('click', () => editItem(item));
        deleteBtn.addEventListener('click', () => deleteItem(item.id));
    });
}

async function handleFormSubmit(event) {
    event.preventDefault();
    
    const itemData = {
        title: titleInput.value.trim(),
        description: descriptionInput.value.trim(),
        completed: completedCheckbox.checked
    };
    
    if (!itemData.title) {
        showToast('Validation Error', 'Title is required', 'error');
        titleInput.focus();
        return;
    }
    
    try {
        showLoading(true);
        
        if (isEditing) {
            // Update existing item
            const itemId = parseInt(itemIdInput.value);
            await updateItem(itemId, itemData);
            showToast('Success', 'Item updated successfully!', 'success');
        } else {
            // Create new item
            await createItem(itemData);
            showToast('Success', 'New item created successfully!', 'success');
        }
        
        resetForm();
        fetchItems();
    } catch (error) {
        console.error('Error saving item:', error);
        showToast('Error', 'Failed to save item. Please try again.', 'error');
        showLoading(false);
    }
}

async function createItem(itemData) {
    const response = await fetch(API_URL, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(itemData)
    });
    
    if (!response.ok) {
        const error = await response.json();
        throw new Error(error.detail || 'Failed to create item');
    }
    
    return await response.json();
}

async function updateItem(itemId, itemData) {
    const response = await fetch(`${API_URL}/${itemId}`, {
        method: 'PUT',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(itemData)
    });
    
    if (!response.ok) {
        const error = await response.json();
        throw new Error(error.detail || 'Failed to update item');
    }
    
    return await response.json();
}

async function deleteItem(itemId) {
    // Create custom confirm dialog
    if (!confirm('Are you sure you want to delete this item? This action cannot be undone.')) {
        return;
    }
    
    try {
        showLoading(true);
        
        const response = await fetch(`${API_URL}/${itemId}`, {
            method: 'DELETE'
        });
        
        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.detail || 'Failed to delete item');
        }
        
        showToast('Success', 'Item deleted successfully!', 'success');
        
        // Remove item from local array
        items = items.filter(item => item.id !== itemId);
        
        // Re-render items
        renderItems(items);
        showLoading(false);
    } catch (error) {
        console.error('Error deleting item:', error);
        showToast('Error', 'Failed to delete item. Please try again.', 'error');
        showLoading(false);
    }
}

function editItem(item) {
    // Set form to edit mode
    isEditing = true;
    formTitle.innerHTML = '<i class="bi bi-pencil-square me-2"></i>Edit Item';
    submitBtn.innerHTML = '<i class="bi bi-save me-2"></i>Update';
    cancelBtn.style.display = 'block';
    
    // Populate form with item data
    itemIdInput.value = item.id;
    titleInput.value = item.title;
    descriptionInput.value = item.description || '';
    completedCheckbox.checked = item.completed;
    
    // Scroll to form
    window.scrollTo({
        top: itemForm.offsetTop - 100,
        behavior: 'smooth'
    });
    
    // Add highlight class to row
    const row = document.getElementById(`item-row-${item.id}`);
    if (row) {
        row.classList.add('highlight-row');
        setTimeout(() => {
            row.classList.remove('highlight-row');
        }, 2000);
    }
    
    // Focus on title input
    titleInput.focus();
}

function resetForm() {
    // Reset form state
    isEditing = false;
    formTitle.innerHTML = '<i class="bi bi-plus-circle me-2"></i>Add New Item';
    submitBtn.innerHTML = '<i class="bi bi-save me-2"></i>Save';
    cancelBtn.style.display = 'none';
    
    // Clear form inputs
    itemForm.reset();
    itemIdInput.value = '';
}

function showToast(title, message, type = 'info') {
    toastTitle.textContent = title;
    toastMessage.textContent = message;
    
    // Remove any existing classes
    toastElement.classList.remove('bg-success', 'bg-danger', 'bg-info', 'bg-warning', 'text-white');
    toastIcon.classList.remove('bi-check-circle-fill', 'bi-exclamation-triangle-fill', 'bi-info-circle-fill');
    
    // Add appropriate styling based on type
    if (type === 'success') {
        toastElement.classList.add('bg-success', 'text-white');
        toastIcon.classList.add('bi-check-circle-fill');
    } else if (type === 'error') {
        toastElement.classList.add('bg-danger', 'text-white');
        toastIcon.classList.add('bi-exclamation-triangle-fill');
    } else {
        toastElement.classList.add('bg-info', 'text-white');
        toastIcon.classList.add('bi-info-circle-fill');
    }
    
    toast.show();
}

function showLoading(isLoading) {
    if (isLoading) {
        loadingSpinner.style.display = 'inline-block';
    } else {
        loadingSpinner.style.display = 'none';
    }
}

// Utility function to prevent XSS
function escapeHtml(str) {
    if (!str) return '';
    return str
        .replace(/&/g, '&amp;')
        .replace(/</g, '&lt;')
        .replace(/>/g, '&gt;')
        .replace(/"/g, '&quot;')
        .replace(/'/g, '&#039;');
}