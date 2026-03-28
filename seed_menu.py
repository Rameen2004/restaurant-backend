from database import get_connection

conn = get_connection()
cursor = conn.cursor()

# 1. OPTIONAL: Clear the table so you don't get duplicates
cursor.execute("TRUNCATE TABLE menu_items")

menu_items = [
    # Format: (Name, Description, Price, Category, Is_Available, Image_URL)
    
    # --- Desi  ---
    ("Chicken Biryani", "Fragrant basmati rice cooked with spiced chicken and herbs", 450.00, "Desi", True, "https://i.postimg.cc/tTc6wBCZ/chicken-biryani.jpg"),
    ("Mutton Karahi", "Tender mutton cooked in a tomato and green chili gravy", 1200.00, "Desi", True, "https://i.postimg.cc/rFVBpg8B/mutton-karahi.jpg"),
    ("Paneer Tikka", "Grilled cubes of cottage cheese marinated in tandoori spices", 350.00, "Desi", True, "https://i.postimg.cc/65qMSPWm/paneer-tikka.jpg"),
    ("Seekh Kabab", "Minced beef skewers grilled over charcoal", 400.00, "Desi", True, "https://i.postimg.cc/QMJgVgNt/seekh-kabab.jpg"),
    ("Butter Chicken", "Creamy tomato-based curry with grilled chicken chunks", 550.00, "Desi", True, "https://i.postimg.cc/XY0yFZPM/butter-chicken.jpg"),
    ("Garlic Naan", "Soft leavened bread topped with fresh garlic and butter", 60.00, "Desi", True, "https://i.postimg.cc/637VW8q6/garlic-naan.jpg"),
    ("Daal Makhani", "Slow-cooked black lentils with cream and butter", 300.00, "Desi", True, "https://i.postimg.cc/NF6HFmwZ/daal-makhni.jpg"),
    ("Nihari", "Slow-cooked beef shank stew with ginger and lemon garnish", 600.00, "Desi", True, "https://i.postimg.cc/T34pRCDQ/nihari.png"),
    ("Samosa Platter", "Crispy pastry triangles filled with spiced potatoes", 150.00, "Desi", True, "https://i.postimg.cc/TwqdW9p0/samosa.jpg"),
    ("Ras Malai", "Soft cheese patties soaked in thickened saffron milk", 200.00, "Desserts", True, "https://i.postimg.cc/kXZmGZfz/rasmalai.jpg"),

    # --- The rest (Image_URL is None/Null) ---
    ("Margherita Pizza", "Classic thin crust with tomato sauce, mozzarella, and basil", 850.00, "Italian", True, None),
    ("Fettuccine Alfredo", "Pasta in a rich parmesan cream sauce with grilled chicken", 700.00, "Italian", True, None),
    ("Lasagna Bolognese", "Layers of pasta with minced beef, bechamel, and cheese", 950.00, "Italian", True, None),
    ("Spaghetti Carbonara", "Pasta with eggs, hard cheese, cured pork, and black pepper", 750.00, "Italian", True, None),
    ("Bruschetta", "Toasted bread topped with tomatoes, garlic, and olive oil", 250.00, "Italian", True, None),
    ("Mushroom Risotto", "Creamy Italian rice cooked with wild mushrooms and truffle oil", 800.00, "Italian", True, None),
    ("Chicken Parmesan", "Breaded chicken breast topped with marinara and melted cheese", 850.00, "Italian", True, None),
    ("Pesto Pasta", "Penne pasta tossed in fresh basil pesto and pine nuts", 650.00, "Italian", True, None),
    ("Minestrone Soup", "Hearty Italian vegetable soup with beans and pasta", 300.00, "Italian", True, None),
    ("Kung Pao Chicken", "Spicy stir-fry chicken with peanuts, vegetables, and chili peppers", 600.00, "Chinese", True, None),
    ("Egg Fried Rice", "Classic stir-fried rice with scrambled eggs and spring onions", 350.00, "Chinese", True, None),
    ("Beef with Broccoli", "Sliced beef stir-fried with fresh broccoli in ginger sauce", 750.00, "Chinese", True, None),
    ("Hot and Sour Soup", "Spicy and tangy soup with mushrooms, tofu, and bamboo shoots", 250.00, "Chinese", True, None),
    ("Vegetable Chow Mein", "Stir-fried noodles with crunchy seasonal vegetables", 450.00, "Chinese", True, None),
    ("Spring Rolls", "Crispy rolls filled with shredded cabbage and carrots", 200.00, "Chinese", True, None),
    ("Manchurian Chicken", "Fried chicken balls in a savory, spicy brown gravy", 650.00, "Chinese", True, None),
    ("Dim Sum Platter", "Assorted steamed dumplings with soy dipping sauce", 500.00, "Chinese", True, None),
    ("Sweet and Sour Prawns", "Crispy prawns tossed in a vibrant pineapple and pepper sauce", 900.00, "Chinese", True, None),
    ("Honey Chili Potato", "Crispy fried potatoes tossed in a sweet and spicy glaze", 300.00, "Chinese", True, None),
    ("Ras Malai", "Soft cheese patties soaked in thickened saffron milk", 200.00, "Desserts", True, None),
    ("Tiramisu", "Coffee-flavored Italian dessert with ladyfingers and mascarpone", 400.00, "Desserts", True, None),
]

# 2. UPDATED QUERY: Added image_url and one more %s
query = """INSERT INTO menu_items (name, description, price, category, is_available, image_url)
           VALUES (%s, %s, %s, %s, %s, %s)"""

cursor.executemany(query, menu_items)
conn.commit()

print(f"Successfully inserted {cursor.rowcount} menu items!")
conn.close()
