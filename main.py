from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from database import get_connection
from models import MenuItemCreate, MenuItemUpdate

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# GET - Read all menu items
@app.get("/menu")
def get_menu():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM menu_items")
    items = cursor.fetchall()
    conn.close()
    return items

# POST - Add a new menu item
@app.post("/menu")
def add_menu_item(item: MenuItemCreate):
    conn = get_connection()
    cursor = conn.cursor()
    # Added 'image_url' and one more '%s'
    query = """INSERT INTO menu_items (name, description, price, category, is_available, image_url)
               VALUES (%s, %s, %s, %s, %s, %s)"""
    # Added item.image_url at the end of the tuple
    cursor.execute(query, (item.name, item.description, item.price, item.category, item.is_available, item.image_url))
    conn.commit()
    new_id = cursor.lastrowid
    conn.close()
    return {"message": "Menu item added successfully", "id": new_id}

# PUT - Update an existing menu item
@app.put("/menu/{item_id}")
def update_menu_item(item_id: int, item: MenuItemUpdate):
    conn = get_connection()
    cursor = conn.cursor()

    fields = []
    values = []

    if item.name is not None:
        fields.append("name = %s")
        values.append(item.name)
    if item.description is not None:
        fields.append("description = %s")
        values.append(item.description)
    if item.price is not None:
        fields.append("price = %s")
        values.append(item.price)
    if item.category is not None:
        fields.append("category = %s")
        values.append(item.category)
    if item.is_available is not None:
        fields.append("is_available = %s")
        values.append(item.is_available)
    
   
    if item.image_url is not None:
        fields.append("image_url = %s")
        values.append(item.image_url)
   
    if not fields:
        conn.close()
        raise HTTPException(status_code=400, detail="No fields to update")

    # Add the item_id at the very end for the WHERE clause
    values.append(item_id)
    
    query = f"UPDATE menu_items SET {', '.join(fields)} WHERE id = %s"
    
    try:
        cursor.execute(query, values)
        conn.commit()

        if cursor.rowcount == 0:
            raise HTTPException(status_code=404, detail="Item not found")

    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        conn.close()

    return {"message": "Menu item updated successfully"}

# DELETE - Remove a menu item
@app.delete("/menu/{item_id}")
def delete_menu_item(item_id: int):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM menu_items WHERE id = %s", (item_id,))
    conn.commit()

    if cursor.rowcount == 0:
        raise HTTPException(status_code=404, detail="Item not found")

    conn.close()
    return {"message": "Menu item deleted successfully"}

