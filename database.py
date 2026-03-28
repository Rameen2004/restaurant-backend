import mysql.connector

def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="rameen@1996",  # ← replace with your MySQL password
        database="restaurant_db"
    )