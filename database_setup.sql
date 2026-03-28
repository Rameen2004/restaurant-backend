CREATE DATABASE restaurant_db;
USE restaurant_db;

CREATE TABLE menu_items (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    description TEXT,
    price DECIMAL(10, 2) NOT NULL,
    category VARCHAR(50) NOT NULL,
    is_available BOOLEAN DEFAULT TRUE
);

USE restaurant_db;
ALTER TABLE menu_items
ADD COLUMN image_url VARCHAR(500) DEFAULT NULL;
