
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import os

from app.database import engine
from app.models.item import Item
import app.routes.item as item_routes

# Create tables in the database
from app.database import Base
Base.metadata.create_all(bind=engine)

# Initialize FastAPI app
app = FastAPI(title="FastAPI CRUD App")

# Mount static files
app.mount("/static", StaticFiles(directory="app/static"), name="static")

# Set up templates
templates = Jinja2Templates(directory="app/templates")

# Include routers
app.include_router(item_routes.router)

# Root endpoint
@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

# Run with: uvicorn app.main:app --reload
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)

"""
# IGNORE THE FOLLOWING SECTION
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import os
import sys
import importlib

from app.database import engine
from app.models.item import Item

# Create tables in the database
from app.database import Base
Base.metadata.create_all(bind=engine)

# Initialize FastAPI app
app = FastAPI(title="FastAPI CRUD App")

# Mount static files
app.mount("/static", StaticFiles(directory="app/static"), name="static")

# Set up templates
templates = Jinja2Templates(directory="app/templates")

# TEMP: Use the solutions for testing
# Import CRUD operations from solutions directory
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from solutions.crud.create import create_item
from solutions.crud.read import get_item, get_items
from solutions.crud.update import update_item
from solutions.crud.delete import delete_item

# Create a temporary crud module that uses solutions
class TempCrud:
    create_item = create_item
    get_item = get_item
    get_items = get_items
    update_item = update_item
    delete_item = delete_item

# Import the router
import app.routes.item as item_routes

# Replace the crud import in the routes with our temporary one
item_routes.crud = TempCrud

# Include routers
app.include_router(item_routes.router)

# Root endpoint
@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

# Run with: uvicorn app.main:app --reload
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
    """