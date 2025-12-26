CREATE DATABASE finance_db

use finance_db

CREATE TABLE IF NOT EXISTS expenses (
  id INT AUTO_INCREMENT PRIMARY KEY,
  category VARCHAR(50) NOT NULL,
  amount FLOAT NOT NULL,
  date DATE NOT NULL
);

CREATE TABLE IF NOT EXISTS sales (
  id INT AUTO_INCREMENT PRIMARY KEY,
  product VARCHAR(50) NOT NULL,
  amount FLOAT NOT NULL,
  month VARCHAR(20) NOT NULL
);

INSERT INTO sales (product, amount, month) VALUES
('Laptop', 1500, 'Jan'),
('Laptop', 1800, 'Feb'),
('Laptop', 1700, 'Mar'),
('Phone', 1200, 'Jan'),
('Phone', 1400, 'Feb'),
('Phone', 1600, 'Mar'),
('Headphones', 400, 'Jan'),
('Headphones', 350, 'Feb'),
('Headphones', 500, 'Mar'),
('Tablet', 800, 'Jan'),
('Tablet', 950, 'Feb'),
('Tablet', 1000, 'Mar');

INSERT INTO expenses (category, amount, date) VALUES
('Rent', 1200, '2025-12-01'),
('Groceries', 320, '2025-12-02'),
('Food', 450, '2025-12-05'),
('Entertainment', 200, '2025-12-07'),
('Utilities', 180, '2025-12-10'),
('Transport', 150, '2025-12-12'),
('Healthcare', 300, '2025-12-15'),
('Education', 250, '2025-12-18');