"""
Run this ONCE to create admin and rider accounts in the database.
These accounts cannot be created via the registration page — by design.

Usage:
  cd backend
  pip install bcrypt
  python seed_users.py
"""

import bcrypt
from database import get_connection


def hash_password(plain: str) -> str:
    return bcrypt.hashpw(plain.encode(), bcrypt.gensalt()).decode()


users = [
    # (name, email, password, role)
    ("Admin User",  "admin@saveur.com",  "Admin@123",  "admin"),
    ("Rider One",   "rider1@saveur.com", "Rider@123",  "rider"),
    ("Rider Two",   "rider2@saveur.com", "Rider@123",  "rider"),
]

conn = get_connection()
cursor = conn.cursor()

# Create the table if it doesn't exist
cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INT AUTO_INCREMENT PRIMARY KEY,
        name VARCHAR(100) NOT NULL,
        email VARCHAR(150) NOT NULL UNIQUE,
        password_hash VARCHAR(255) NOT NULL,
        role ENUM('customer', 'admin', 'rider') NOT NULL DEFAULT 'customer',
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
""")

inserted = 0
skipped  = 0

for name, email, password, role in users:
    cursor.execute("SELECT id FROM users WHERE email = %s", (email,))
    if cursor.fetchone():
        print(f"  SKIP  {email} (already exists)")
        skipped += 1
        continue

    hashed = hash_password(password)
    cursor.execute(
        "INSERT INTO users (name, email, password_hash, role) VALUES (%s, %s, %s, %s)",
        (name, email, hashed, role)
    )
    print(f"  OK    {email} ({role})")
    inserted += 1

conn.commit()
conn.close()
print(f"\nDone — {inserted} inserted, {skipped} skipped.")
print("\nLogin credentials:")
for name, email, password, role in users:
    print(f"  [{role}]  {email}  /  {password}")