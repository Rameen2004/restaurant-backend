# Restaurant-menu-backend
Software Engineering - Group 7
## Project Overview
Backend for the Restaurant Management mobile application.
This sprint covers Menu Management (FR-4) — Finance Staff can
add, update, view, and delete menu items.

---

## Tech Stack
- Backend: Python + FastAPI
- Database: MySQL

---

## Setup Instructions

### Step 1 - Clone the Repository
git clone https://github.com/YOURUSERNAME/restaurant-backend.git
cd restaurant-backend

### Step 2 - Create Virtual Environment
python -m venv venv
venv\Scripts\activate

### Step 3 - Install Packages
pip install -r requirements.txt

### Step 4 - Install MySQL
- Download from https://dev.mysql.com/downloads/installer/
- Choose Server Only
- Set a root password and remember it

### Step 5 - Create Database and Table
- Open terminal and run: mysql -u root -p
- Copy and run everything from database_setup.sql

### Step 6 - Update Your Password
- Open database.py
- Replace YOUR_PASSWORD_HERE with your MySQL root password

### Step 7 - Run the Server
uvicorn main:app --reload

### Step 8 - Seed the Database
python seed_menu.py
You should see: Successfully inserted 30 menu items!

### Step 9 - Test the API
Open: http://localhost:8000/docs

---
