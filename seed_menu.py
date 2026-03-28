# from database import get_connection

# conn = get_connection()
# cursor = conn.cursor()

# # 1. OPTIONAL: Clear the table so you don't get duplicates
# cursor.execute("TRUNCATE TABLE menu_items")

# menu_items = [
#     # Format: (Name, Description, Price, Category, Is_Available, Image_URL)
    
#     # --- Desi  ---
#     ("Chicken Biryani", "Fragrant basmati rice cooked with spiced chicken and herbs", 450.00, "Desi", True, "https://i.postimg.cc/tTc6wBCZ/chicken-biryani.jpg"),
#     ("Mutton Karahi", "Tender mutton cooked in a tomato and green chili gravy", 1200.00, "Desi", True, "https://i.postimg.cc/rFVBpg8B/mutton-karahi.jpg"),
#     ("Paneer Tikka", "Grilled cubes of cottage cheese marinated in tandoori spices", 350.00, "Desi", True, "https://i.postimg.cc/65qMSPWm/paneer-tikka.jpg"),
#     ("Seekh Kabab", "Minced beef skewers grilled over charcoal", 400.00, "Desi", True, "https://i.postimg.cc/QMJgVgNt/seekh-kabab.jpg"),
#     ("Butter Chicken", "Creamy tomato-based curry with grilled chicken chunks", 550.00, "Desi", True, "https://i.postimg.cc/XY0yFZPM/butter-chicken.jpg"),
#     ("Garlic Naan", "Soft leavened bread topped with fresh garlic and butter", 60.00, "Desi", True, "https://i.postimg.cc/637VW8q6/garlic-naan.jpg"),
#     ("Daal Makhani", "Slow-cooked black lentils with cream and butter", 300.00, "Desi", True, "https://i.postimg.cc/NF6HFmwZ/daal-makhni.jpg"),
#     ("Nihari", "Slow-cooked beef shank stew with ginger and lemon garnish", 600.00, "Desi", True, "https://i.postimg.cc/T34pRCDQ/nihari.png"),
#     ("Samosa Platter", "Crispy pastry triangles filled with spiced potatoes", 150.00, "Desi", True, "https://i.postimg.cc/TwqdW9p0/samosa.jpg"),
#     ("Ras Malai", "Soft cheese patties soaked in thickened saffron milk", 200.00, "Desserts", True, "https://i.postimg.cc/kXZmGZfz/rasmalai.jpg"),

#     # --- The rest (Image_URL is None/Null) ---
#     ("Margherita Pizza", "Classic thin crust with tomato sauce, mozzarella, and basil", 850.00, "Italian", True, None),
#     ("Fettuccine Alfredo", "Pasta in a rich parmesan cream sauce with grilled chicken", 700.00, "Italian", True, None),
#     ("Lasagna Bolognese", "Layers of pasta with minced beef, bechamel, and cheese", 950.00, "Italian", True, None),
#     ("Spaghetti Carbonara", "Pasta with eggs, hard cheese, cured pork, and black pepper", 750.00, "Italian", True, None),
#     ("Bruschetta", "Toasted bread topped with tomatoes, garlic, and olive oil", 250.00, "Italian", True, None),
#     ("Mushroom Risotto", "Creamy Italian rice cooked with wild mushrooms and truffle oil", 800.00, "Italian", True, None),
#     ("Chicken Parmesan", "Breaded chicken breast topped with marinara and melted cheese", 850.00, "Italian", True, None),
#     ("Pesto Pasta", "Penne pasta tossed in fresh basil pesto and pine nuts", 650.00, "Italian", True, None),
#     ("Minestrone Soup", "Hearty Italian vegetable soup with beans and pasta", 300.00, "Italian", True, None),
#     ("Kung Pao Chicken", "Spicy stir-fry chicken with peanuts, vegetables, and chili peppers", 600.00, "Chinese", True, None),
#     ("Egg Fried Rice", "Classic stir-fried rice with scrambled eggs and spring onions", 350.00, "Chinese", True, None),
#     ("Beef with Broccoli", "Sliced beef stir-fried with fresh broccoli in ginger sauce", 750.00, "Chinese", True, None),
#     ("Hot and Sour Soup", "Spicy and tangy soup with mushrooms, tofu, and bamboo shoots", 250.00, "Chinese", True, None),
#     ("Vegetable Chow Mein", "Stir-fried noodles with crunchy seasonal vegetables", 450.00, "Chinese", True, None),
#     ("Spring Rolls", "Crispy rolls filled with shredded cabbage and carrots", 200.00, "Chinese", True, None),
#     ("Manchurian Chicken", "Fried chicken balls in a savory, spicy brown gravy", 650.00, "Chinese", True, None),
#     ("Dim Sum Platter", "Assorted steamed dumplings with soy dipping sauce", 500.00, "Chinese", True, None),
#     ("Sweet and Sour Prawns", "Crispy prawns tossed in a vibrant pineapple and pepper sauce", 900.00, "Chinese", True, None),
#     ("Honey Chili Potato", "Crispy fried potatoes tossed in a sweet and spicy glaze", 300.00, "Chinese", True, None),
#     ("Ras Malai", "Soft cheese patties soaked in thickened saffron milk", 200.00, "Desserts", True, None),
#     ("Tiramisu", "Coffee-flavored Italian dessert with ladyfingers and mascarpone", 400.00, "Desserts", True, None),
# ]

# # 2. UPDATED QUERY: Added image_url and one more %s
# query = """INSERT INTO menu_items (name, description, price, category, is_available, image_url)
#            VALUES (%s, %s, %s, %s, %s, %s)"""

# cursor.executemany(query, menu_items)
# conn.commit()

# print(f"Successfully inserted {cursor.rowcount} menu items!")
# conn.close()



from database import get_connection

conn = get_connection()
cursor = conn.cursor()

cursor.execute("TRUNCATE TABLE menu_items")

menu_items = [
    # --- Desi ---
    ("Chicken Biryani", "Fragrant basmati rice cooked with spiced chicken and herbs", 450.00, "Desi", True, "https://i.postimg.cc/tTc6wBCZ/chicken-biryani.jpg"),
    ("Mutton Karahi", "Tender mutton cooked in a tomato and green chili gravy", 1200.00, "Desi", True, "https://i.postimg.cc/rFVBpg8B/mutton-karahi.jpg"),
    ("Paneer Tikka", "Grilled cubes of cottage cheese marinated in tandoori spices", 350.00, "Desi", True, "https://i.postimg.cc/65qMSPWm/paneer-tikka.jpg"),
    ("Seekh Kabab", "Minced beef skewers grilled over charcoal", 400.00, "Desi", True, "https://i.postimg.cc/QMJgVgNt/seekh-kabab.jpg"),
    ("Butter Chicken", "Creamy tomato-based curry with grilled chicken chunks", 550.00, "Desi", True, "https://i.postimg.cc/XY0yFZPM/butter-chicken.jpg"),
    ("Garlic Naan", "Soft leavened bread topped with fresh garlic and butter", 60.00, "Desi", True, "https://i.postimg.cc/637VW8q6/garlic-naan.jpg"),
    ("Daal Makhani", "Slow-cooked black lentils with cream and butter", 300.00, "Desi", True, "https://i.postimg.cc/NF6HFmwZ/daal-makhni.jpg"),
    ("Nihari", "Slow-cooked beef shank stew with ginger and lemon garnish", 600.00, "Desi", True, "https://i.postimg.cc/T34pRCDQ/nihari.png"),
    ("Samosa Platter", "Crispy pastry triangles filled with spiced potatoes", 150.00, "Desi", True, "https://i.postimg.cc/TwqdW9p0/samosa.jpg"),

    # --- Desserts ---
    ("Ras Malai", "Soft cheese patties soaked in thickened saffron milk", 200.00, "Desserts", True, "https://i.postimg.cc/kXZmGZfz/rasmalai.jpg"),
    ("Tiramisu", "Coffee-flavored Italian dessert with ladyfingers and mascarpone", 400.00, "Desserts", True, "https://images.unsplash.com/photo-1571877227200-a0d98ea607e9?w=600&q=80"),

    # --- Italian ---
    ("Margherita Pizza", "Classic thin crust with tomato sauce, mozzarella, and basil", 850.00, "Italian", True, "https://images.unsplash.com/photo-1574071318508-1cdbab80d002?w=600&q=80"),
    ("Fettuccine Alfredo", "Pasta in a rich parmesan cream sauce with grilled chicken", 700.00, "Italian", True, "https://images.unsplash.com/photo-1645112411341-6c4fd023714a?w=600&q=80"),
    ("Lasagna Bolognese", "Layers of pasta with minced beef, bechamel, and cheese", 950.00, "Italian", True, "https://images.unsplash.com/photo-1619895092538-128341789043?w=600&q=80"),
    ("Spaghetti Carbonara", "Pasta with eggs, hard cheese, cured pork, and black pepper", 750.00, "Italian", True, "https://images.unsplash.com/photo-1612874742237-6526221588e3?w=600&q=80"),
    ("Bruschetta", "Toasted bread topped with tomatoes, garlic, and olive oil", 250.00, "Italian", True, "https://images.unsplash.com/photo-1572695157366-5e585ab2b69f?w=600&q=80"),
    ("Mushroom Risotto", "Creamy Italian rice cooked with wild mushrooms and truffle oil", 800.00, "Italian", True, "https://www.thespruceeats.com/thmb/3X6VLB4zEaWD9arlTdtOfyQIsy0=/1500x0/filters:no_upscale():max_bytes(150000):strip_icc():format(webp)/SES-mushroom-risotto-recipe-996005-hero-01-85f8cef9cf8042e8afbaa9d2e46c1fa8.jpg"),
    ("Chicken Parmesan", "Breaded chicken breast topped with marinara and melted cheese", 850.00, "Italian", True, "https://images.unsplash.com/photo-1632778149955-e80f8ceca2e8?w=600&q=80"),
    ("Pesto Pasta", "Penne pasta tossed in fresh basil pesto and pine nuts", 650.00, "Italian", True, "https://images.unsplash.com/photo-1473093295043-cdd812d0e601?w=600&q=80"),
    ("Minestrone Soup", "Hearty Italian vegetable soup with beans and pasta", 300.00, "Italian", True, "https://www.yourhomemadehealthy.com/wp-content/uploads/2022/06/Chicken-Minestrone-Soup-20.jpg"),

    # --- Chinese ---
    ("Kung Pao Chicken", "Spicy stir-fry chicken with peanuts, vegetables, and chili peppers", 600.00, "Chinese", True, "https://thegingeredwhisk.com/wp-content/uploads/2017/03/Kung-Poa-Chicken-16-683x1024.jpg"),
    ("Egg Fried Rice", "Classic stir-fried rice with scrambled eggs and spring onions", 350.00, "Chinese", True, "https://www.ericajulson.com/wp-content/uploads/2017/07/Easy-Egg-Fried-Rice-7.jpg"),
    ("Beef with Broccoli", "Sliced beef stir-fried with fresh broccoli in ginger sauce", 750.00, "Chinese", True, "https://takestwoeggs.com/wp-content/uploads/2025/03/Chinese-Beef-and-Broccoli-Plate-overhead.webp"),
    ("Hot and Sour Soup", "Spicy and tangy soup with mushrooms, tofu, and bamboo shoots", 250.00, "Chinese", True, "https://www.chilitochoc.com/wp-content/uploads/2021/01/chinese-hot-and-sour-soup-1.jpg"),
    ("Vegetable Chow Mein", "Stir-fried noodles with crunchy seasonal vegetables", 450.00, "Chinese", True, "https://jackslobodian.com/wp-content/uploads/2021/03/Vegetable-Vegan-Chow-Mein-2-1200x798.jpg"),
    ("Spring Rolls", "Crispy rolls filled with shredded cabbage and carrots", 200.00, "Chinese", True, "https://www.cubesnjuliennes.com/wp-content/uploads/2021/01/Veggie-Spring-Rolls.jpg"),
    ("Manchurian Chicken", "Fried chicken balls in a savory, spicy brown gravy", 650.00, "Chinese", True, "https://www.foodforfitness.co.uk/wp-content/smush-webp/2025/06/Manchurian-Chicken-Recipe-3-1024x683.jpg.webp"),
    ("Dim Sum Platter", "Assorted steamed dumplings with soy dipping sauce", 500.00, "Chinese", True, "https://images.unsplash.com/photo-1563245372-f21724e3856d?w=600&q=80"),
    ("Sweet and Sour Prawns", "Crispy prawns tossed in a vibrant pineapple and pepper sauce", 900.00, "Chinese", True, "https://mymorningmocha.com/wp-content/uploads/2023/03/Homemade-sweet-and-sour-king-prawns.jpg"),
    ("Honey Chili Potato", "Crispy fried potatoes tossed in a sweet and spicy glaze", 300.00, "Chinese", True, "https://i.pinimg.com/736x/5d/bd/9a/5dbd9a2f5a44fe6a6edd933e2ccd4ed4.jpg"),
]

query = """INSERT INTO menu_items (name, description, price, category, is_available, image_url)
           VALUES (%s, %s, %s, %s, %s, %s)"""

cursor.executemany(query, menu_items)
conn.commit()

print(f"Successfully inserted {cursor.rowcount} menu items!")
conn.close()