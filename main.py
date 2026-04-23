from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from database import get_connection
from models import (
    MenuItemCreate, MenuItemUpdate,
    UserRegister, UserLogin, GoogleLogin, PhoneLookup,
    SendOTP, VerifyOTP, ResetPasswordOTP
)
import bcrypt
import random
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime, timedelta
import firebase_admin
from firebase_admin import credentials, auth as firebase_auth

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# ── Firebase Admin SDK init ───────────────────────────────────────────────────
if not firebase_admin._apps:
    cred = credentials.Certificate("serviceAccountKey.json")
    firebase_admin.initialize_app(cred)

# ── Gmail SMTP config ─────────────────────────────────────────────────────────
GMAIL_USER     = "saveur999@gmail.com"
GMAIL_APP_PASS = "tpqclbfuerhulrsv"

# In-memory OTP store
otp_store: dict = {}


def send_otp_email(to_email: str, otp: str):
    msg = MIMEMultipart("alternative")
    msg["Subject"] = "Your Saveur Password Reset Code"
    msg["From"]    = GMAIL_USER
    msg["To"]      = to_email

    html = f"""
    <div style="font-family: Georgia, serif; max-width: 420px; margin: 0 auto; padding: 32px; background: #faf9f7; border-radius: 16px;">
      <h2 style="color: #2b2b2b; font-size: 22px; margin-bottom: 8px;">Password Reset</h2>
      <p style="color: #777; font-size: 14px; margin-bottom: 24px;">
        Use the code below to reset your Saveur password. It expires in <strong>10 minutes</strong>.
      </p>
      <div style="background: #fff; border: 1px dashed #e0dbd4; border-radius: 12px; padding: 24px; text-align: center;">
        <span style="font-size: 36px; font-weight: bold; letter-spacing: 10px; color: #2b2b2b;">{otp}</span>
      </div>
      <p style="color: #aaa; font-size: 12px; margin-top: 24px;">
        If you didn't request this, you can safely ignore this email.
      </p>
    </div>
    """

    msg.attach(MIMEText(html, "html"))

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(GMAIL_USER, GMAIL_APP_PASS)
        server.sendmail(GMAIL_USER, to_email, msg.as_string())


# ══════════════════════════════════════════════════════
#  AUTH ENDPOINTS
# ══════════════════════════════════════════════════════

@app.post("/auth/register")
def register(user: UserRegister):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT id FROM users WHERE email = %s", (user.email,))
    if cursor.fetchone():
        conn.close()
        raise HTTPException(status_code=409, detail="Email already registered")

    cursor.execute("SELECT id FROM users WHERE phone = %s", (user.phone,))
    if cursor.fetchone():
        conn.close()
        raise HTTPException(status_code=409, detail="Phone number already registered")

    password_hash = bcrypt.hashpw(user.password.encode(), bcrypt.gensalt()).decode()

    cursor.execute(
        "INSERT INTO users (name, email, phone, password_hash, role) VALUES (%s, %s, %s, %s, 'customer')",
        (user.name, user.email, user.phone, password_hash)
    )
    conn.commit()
    new_id = cursor.lastrowid
    conn.close()

    # ── Create user in Firebase so email/password login works ─────────────────
    try:
        firebase_auth.create_user(
            email=user.email,
            password=user.password,
            display_name=user.name,
        )
    except firebase_auth.EmailAlreadyExistsError:
        pass  # Already exists in Firebase, that's fine

    return {
        "message": "Account created successfully",
        "user": {"id": new_id, "name": user.name, "email": user.email, "role": "customer"}
    }


@app.post("/auth/login")
def login(credentials: UserLogin):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    if credentials.email:
        cursor.execute(
            "SELECT * FROM users WHERE email = %s AND role = %s",
            (credentials.email, credentials.role)
        )
    elif credentials.phone:
        cursor.execute(
            "SELECT * FROM users WHERE phone = %s AND role = %s",
            (credentials.phone, credentials.role)
        )
    else:
        conn.close()
        raise HTTPException(status_code=400, detail="Email or phone required")

    user = cursor.fetchone()
    conn.close()

    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    if credentials.password != '__firebase_verified__':
        if not bcrypt.checkpw(credentials.password.encode(), user["password_hash"].encode()):
            raise HTTPException(status_code=401, detail="Invalid credentials")

    return {
        "message": "Login successful",
        "user": {
            "id":    user["id"],
            "name":  user["name"],
            "email": user["email"],
            "role":  user["role"]
        }
    }


@app.post("/auth/lookup-by-phone")
def lookup_by_phone(body: PhoneLookup):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT email FROM users WHERE phone = %s", (body.phone,))
    user = cursor.fetchone()
    conn.close()

    if not user:
        raise HTTPException(status_code=404)

    return {"email": user["email"]}


@app.post("/auth/google-login")
def google_login(user: GoogleLogin):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT * FROM users WHERE email = %s", (user.email,))
    existing = cursor.fetchone()

    if existing:
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

    cursor.execute(
        "INSERT INTO users (name, email, phone, password_hash, role) VALUES (%s, %s, NULL, %s, 'customer')",
        (user.name, user.email, f"google_uid:{user.uid}")
    )
    conn.commit()
    new_id = cursor.lastrowid
    conn.close()

    return {
        "message": "Account created via Google",
        "user": {"id": new_id, "name": user.name, "email": user.email, "role": "customer"}
    }


# ── OTP Password Reset Endpoints ──────────────────────────────────────────────

@app.post("/auth/send-otp")
def send_otp(body: SendOTP):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT id FROM users WHERE email = %s", (body.email,))
    user = cursor.fetchone()
    conn.close()

    if not user:
        return {"message": "If that email is registered, an OTP has been sent."}

    otp = str(random.randint(100000, 999999))
    otp_store[body.email] = {
        "otp":        otp,
        "expires_at": datetime.utcnow() + timedelta(minutes=10)
    }

    try:
        send_otp_email(body.email, otp)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to send email: {str(e)}")

    return {"message": "If that email is registered, an OTP has been sent."}


@app.post("/auth/verify-otp")
def verify_otp(body: VerifyOTP):
    entry = otp_store.get(body.email)

    if not entry:
        raise HTTPException(status_code=400, detail="No OTP requested for this email.")

    if datetime.utcnow() > entry["expires_at"]:
        otp_store.pop(body.email, None)
        raise HTTPException(status_code=400, detail="OTP has expired. Please request a new one.")

    if entry["otp"] != body.otp:
        raise HTTPException(status_code=400, detail="Incorrect OTP.")

    return {"message": "OTP verified."}


@app.post("/auth/reset-password-otp")
def reset_password_otp(body: ResetPasswordOTP):
    entry = otp_store.get(body.email)

    if not entry:
        raise HTTPException(status_code=400, detail="No OTP requested for this email.")

    if datetime.utcnow() > entry["expires_at"]:
        otp_store.pop(body.email, None)
        raise HTTPException(status_code=400, detail="OTP has expired. Please request a new one.")

    if entry["otp"] != body.otp:
        raise HTTPException(status_code=400, detail="Incorrect OTP.")

    if len(body.new_password) < 8:
        raise HTTPException(status_code=400, detail="Password must be at least 8 characters.")

    # ── 1. Update password in MySQL ───────────────────────────────────────────
    new_hash = bcrypt.hashpw(body.new_password.encode(), bcrypt.gensalt()).decode()
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    # Also grab the user's role so we know if Firebase sync is needed
    cursor.execute("SELECT role FROM users WHERE email = %s", (body.email,))
    user = cursor.fetchone()

    cursor.execute(
        "UPDATE users SET password_hash = %s WHERE email = %s",
        (new_hash, body.email)
    )
    conn.commit()
    conn.close()

    # ── 2. Update password in Firebase (customers only) ───────────────────────
    # Admins and riders don't have Firebase accounts so skip them
    if user and user["role"] == "customer":
        try:
            firebase_user = firebase_auth.get_user_by_email(body.email)
            firebase_auth.update_user(firebase_user.uid, password=body.new_password)
        except firebase_auth.UserNotFoundError:
            # User exists in MySQL but not Firebase (registered before Firebase sync was added)
            # Create them in Firebase now with the new password
            try:
                firebase_auth.create_user(email=body.email, password=body.new_password)
            except Exception as e:
                print(f"Firebase user creation during reset failed: {e}")
        except Exception as e:
            # Don't block the response — MySQL already updated
            print(f"Firebase password update failed: {e}")

    # ── 3. Consume the OTP ────────────────────────────────────────────────────
    otp_store.pop(body.email, None)

    return {"message": "Password updated successfully."}


# ══════════════════════════════════════════════════════
#  MENU ENDPOINTS
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