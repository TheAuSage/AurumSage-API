import sqlite3
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

# Connect to SQLite database
conn = sqlite3.connect("database.db", check_same_thread=False)
cursor = conn.cursor()

# Create table if it doesn't exist
cursor.execute('''
    CREATE TABLE IF NOT EXISTS items (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        price REAL NOT NULL,
        in_stock BOOLEAN NOT NULL
    )
''')
conn.commit()

# Define request model
class Item(BaseModel):
    name: str
    price: float
    in_stock: bool

# POST: Add item to database
@app.post("/add-item/")
async def add_item(item: Item):
    cursor.execute(
        "INSERT INTO items (name, price, in_stock) VALUES (?, ?, ?)",
        (item.name, item.price, item.in_stock),
    )
    conn.commit()
    return {"message": f"Added {item.name} at ${item.price}"}

# GET: Fetch all items
@app.get("/items/")
async def get_items():
    cursor.execute("SELECT * FROM items")
    items = cursor.fetchall()
    return {"items": items}
