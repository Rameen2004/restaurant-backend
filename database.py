import mysql.connector

def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="#",  # ← replace with your MySQL password
        database="restaurant_db"
    )