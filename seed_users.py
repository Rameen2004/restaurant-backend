import bcrypt
from database import get_connection


def hash_password(plain: str) -> str:
    return bcrypt.hashpw(plain.encode(), bcrypt.gensalt()).decode()

users = [
    ("Admin User", "admin@saveur.com",               "+923001111111", "Admin@123", "admin"),
    ("Admin 2",    "khadijaabbas.6940ams@gmail.com", "+923361322128", "123456",    "admin"),
    ("Rider One",  "ka09196@st.habib.edu.pk",         "+923032931186", "123456",   "rider"),
    ("Rider Two",  "rider2@saveur.com",               "+923003333333", "Rider@123", "rider"),
]

conn = get_connection()
cursor = conn.cursor()

cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id            INT AUTO_INCREMENT PRIMARY KEY,
        name          VARCHAR(100)  NOT NULL,
        email         VARCHAR(150)  NOT NULL UNIQUE,
        phone         VARCHAR(20)   NULL UNIQUE,
        password_hash VARCHAR(255)  NOT NULL,
        role          ENUM('customer', 'admin', 'rider') NOT NULL DEFAULT 'customer',
        created_at    TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
""")

inserted = 0
skipped  = 0

for name, email, phone, password, role in users:
    cursor.execute("SELECT id FROM users WHERE email = %s", (email,))
    if cursor.fetchone():
        print(f"  SKIP  {email} (already exists)")
        skipped += 1
        continue

    hashed = hash_password(password)
    cursor.execute(
        "INSERT INTO users (name, email, phone, password_hash, role) VALUES (%s, %s, %s, %s, %s)",
        (name, email, phone, hashed, role)
    )
    print(f"  OK    {email} ({role})")
    inserted += 1

conn.commit()
conn.close()
print(f"\nDone — {inserted} inserted, {skipped} skipped.")
print("\nLogin credentials:")
for name, email, phone, password, role in users:
    print(f"  [{role}]  {email}  /  {phone}  /  {password}")