from database import get_connection

conn = get_connection()
cursor = conn.cursor()

menu_items = [
    # Desi
    ("Chicken Biryani", "Fragrant basmati rice cooked with spiced chicken and herbs", 450.00, "Desi", True),
    ("Mutton Karahi", "Tender mutton cooked in a tomato and green chili gravy", 1200.00, "Desi", True),
    ("Paneer Tikka", "Grilled cubes of cottage cheese marinated in tandoori spices", 350.00, "Desi", True),
    ("Seekh Kabab", "Minced beef skewers grilled over charcoal", 400.00, "Desi", True),
    ("Butter Chicken", "Creamy tomato-based curry with grilled chicken chunks", 550.00, "Desi", True),
    ("Garlic Naan", "Soft leavened bread topped with fresh garlic and butter", 60.00, "Desi", True),
    ("Daal Makhani", "Slow-cooked black lentils with cream and butter", 300.00, "Desi", True),
    ("Nihari", "Slow-cooked beef shank stew with ginger and lemon garnish", 600.00, "Desi", True),
    ("Samosa Platter", "Crispy pastry triangles filled with spiced potatoes", 150.00, "Desi", True),
    # Italian
    ("Margherita Pizza", "Classic thin crust with tomato sauce, mozzarella, and basil", 850.00, "Italian", True),
    ("Fettuccine Alfredo", "Pasta in a rich parmesan cream sauce with grilled chicken", 700.00, "Italian", True),
    ("Lasagna Bolognese", "Layers of pasta with minced beef, bechamel, and cheese", 950.00, "Italian", True),
    ("Spaghetti Carbonara", "Pasta with eggs, hard cheese, cured pork, and black pepper", 750.00, "Italian", True),
    ("Bruschetta", "Toasted bread topped with tomatoes, garlic, and olive oil", 250.00, "Italian", True),
    ("Mushroom Risotto", "Creamy Italian rice cooked with wild mushrooms and truffle oil", 800.00, "Italian", True),
    ("Chicken Parmesan", "Breaded chicken breast topped with marinara and melted cheese", 850.00, "Italian", True),
    ("Pesto Pasta", "Penne pasta tossed in fresh basil pesto and pine nuts", 650.00, "Italian", True),
    ("Minestrone Soup", "Hearty Italian vegetable soup with beans and pasta", 300.00, "Italian", True),
    # Chinese
    ("Kung Pao Chicken", "Spicy stir-fry chicken with peanuts, vegetables, and chili peppers", 600.00, "Chinese", True),
    ("Egg Fried Rice", "Classic stir-fried rice with scrambled eggs and spring onions", 350.00, "Chinese", True),
    ("Beef with Broccoli", "Sliced beef stir-fried with fresh broccoli in ginger sauce", 750.00, "Chinese", True),
    ("Hot and Sour Soup", "Spicy and tangy soup with mushrooms, tofu, and bamboo shoots", 250.00, "Chinese", True),
    ("Vegetable Chow Mein", "Stir-fried noodles with crunchy seasonal vegetables", 450.00, "Chinese", True),
    ("Spring Rolls", "Crispy rolls filled with shredded cabbage and carrots", 200.00, "Chinese", True),
    ("Manchurian Chicken", "Fried chicken balls in a savory, spicy brown gravy", 650.00, "Chinese", True),
    ("Dim Sum Platter", "Assorted steamed dumplings with soy dipping sauce", 500.00, "Chinese", True),
    ("Sweet and Sour Prawns", "Crispy prawns tossed in a vibrant pineapple and pepper sauce", 900.00, "Chinese", True),
    ("Honey Chili Potato", "Crispy fried potatoes tossed in a sweet and spicy glaze", 300.00, "Chinese", True),
    # Desserts
    ("Ras Malai", "Soft cheese patties soaked in thickened saffron milk", 200.00, "Desserts", True),
    ("Tiramisu", "Coffee-flavored Italian dessert with ladyfingers and mascarpone", 400.00, "Desserts", True),
]

query = """INSERT INTO menu_items (name, description, price, category, is_available)
           VALUES (%s, %s, %s, %s, %s)"""

cursor.executemany(query, menu_items)
conn.commit()

print(f"Successfully inserted {cursor.rowcount} menu items!")
conn.close()
