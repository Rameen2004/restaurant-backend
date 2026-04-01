from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from database import get_connection
from models import MenuItemCreate, MenuItemUpdate, UserRegister, UserLogin, GoogleLogin
import bcrypt

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


# ══════════════════════════════════════════════════════
#  AUTH ENDPOINTS
# ══════════════════════════════════════════════════════

@app.post("/auth/register")
def register(user: UserRegister):
    """
    Only customers can self-register.
    Admin and rider accounts must be pre-seeded in the database.
    """
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    # Check if email already exists
    cursor.execute("SELECT id FROM users WHERE email = %s", (user.email,))
    if cursor.fetchone():
        conn.close()
        raise HTTPException(status_code=409, detail="Email already registered")

    # Hash password
    password_hash = bcrypt.hashpw(user.password.encode(), bcrypt.gensalt()).decode()

    # Insert as customer (role is always 'customer' for self-registration)
    cursor.execute(
        "INSERT INTO users (name, email, password_hash, role) VALUES (%s, %s, %s, 'customer')",
        (user.name, user.email, password_hash)
    )
    conn.commit()
    new_id = cursor.lastrowid
    conn.close()

    return {
        "message": "Account created successfully",
        "user": {"id": new_id, "name": user.name, "email": user.email, "role": "customer"}
    }


@app.post("/auth/login")
def login(credentials: UserLogin):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute(
        "SELECT * FROM users WHERE email = %s AND role = %s",
        (credentials.email, credentials.role)
    )
    user = cursor.fetchone()
    conn.close()

    if not user:
        raise HTTPException(status_code=401, detail="Invalid email or password")

    # If Firebase already verified the password (customer login), skip bcrypt check
    if credentials.password != '__firebase_verified__':
        if not bcrypt.checkpw(credentials.password.encode(), user["password_hash"].encode()):
            raise HTTPException(status_code=401, detail="Invalid email or password")

    return {
        "message": "Login successful",
        "user": {
            "id": user["id"],
            "name": user["name"],
            "email": user["email"],
            "role": user["role"]
        }
    }

# ```

# **The flow is now:**
# ```
# Customer login:
#   Firebase checks password ✅ (always current, even after reset)
#   MySQL returns name/role/id ✅

# Admin/Rider login:
#   MySQL checks password directly ✅ (unchanged)


# ─────────────────────────────────────────────────────────────────────────────
# ADD THIS TO YOUR main.py  (paste after your existing /auth/login endpoint)
# Also add GoogleLogin to your models.py imports (model shown below)
# ─────────────────────────────────────────────────────────────────────────────

# In models.py, add this class:
#
# class GoogleLogin(BaseModel):
#     name: str
#     email: str
#     uid: str    # Firebase UID

# ─────────────────────────────────────────────────────────────────────────────
# In main.py, add this import at the top:
#   from models import ..., GoogleLogin
#
# Then add this endpoint:
# ─────────────────────────────────────────────────────────────────────────────

@app.post("/auth/google-login")
def google_login(user: GoogleLogin):
    """
    Called after Firebase Google sign-in succeeds on the frontend.
    - If the email already exists in our DB → log them in (return their record).
    - If new → auto-create a customer account (no password needed for Google users).
    Google users are always customers. Admin/rider accounts use email+password only.
    """
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    # Check if user already exists
    cursor.execute("SELECT * FROM users WHERE email = %s", (user.email,))
    existing = cursor.fetchone()

    if existing:
        # Already registered — just return their info
        conn.close()
        return {
            "message": "Login successful",
            "user": {
                "id":    existing["id"],
                "name":  existing["name"],
                "email": existing["email"],
                "role":  existing["role"],
            }
        }

    # New Google user — auto-register as customer
    # We store a placeholder password_hash since they'll always use Google to log in
    cursor.execute(
        "INSERT INTO users (name, email, password_hash, role) VALUES (%s, %s, %s, 'customer')",
        (user.name, user.email, f"google_uid:{user.uid}")
    )
    conn.commit()
    new_id = cursor.lastrowid
    conn.close()

    return {
        "message": "Account created via Google",
        "user": {
            "id":    new_id,
            "name":  user.name,
            "email": user.email,
            "role":  "customer",
        }
    }


# ══════════════════════════════════════════════════════
#  MENU ENDPOINTS (unchanged from your partner's work)
# ══════════════════════════════════════════════════════

@app.get("/menu")
def get_menu():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM menu_items")
    items = cursor.fetchall()
    conn.close()
    return items


@app.post("/menu")
def add_menu_item(item: MenuItemCreate):
    conn = get_connection()
    cursor = conn.cursor()
    query = """INSERT INTO menu_items (name, description, price, category, is_available, image_url)
               VALUES (%s, %s, %s, %s, %s, %s)"""
    cursor.execute(query, (item.name, item.description, item.price, item.category, item.is_available, item.image_url))
    conn.commit()
    new_id = cursor.lastrowid
    conn.close()
    return {"message": "Menu item added successfully", "id": new_id}


@app.put("/menu/{item_id}")
def update_menu_item(item_id: int, item: MenuItemUpdate):
    conn = get_connection()
    cursor = conn.cursor()

    fields = []
    values = []

    if item.name is not None:
        fields.append("name = %s"); values.append(item.name)
    if item.description is not None:
        fields.append("description = %s"); values.append(item.description)
    if item.price is not None:
        fields.append("price = %s"); values.append(item.price)
    if item.category is not None:
        fields.append("category = %s"); values.append(item.category)
    if item.is_available is not None:
        fields.append("is_available = %s"); values.append(item.is_available)
    if item.image_url is not None:
        fields.append("image_url = %s"); values.append(item.image_url)

    if not fields:
        conn.close()
        raise HTTPException(status_code=400, detail="No fields to update")

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