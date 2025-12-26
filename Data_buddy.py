import random
import mysql.connector
from datetime import datetime, timedelta

# Connect to MySQL
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="tiger",
    database="finance_db"
)
cursor = conn.cursor()

# Categories and products
expense_categories = ["Rent", "Groceries", "Food", "Entertainment", "Utilities", "Transport", "Healthcare", "Education", "Misc"]
products = ["Laptop", "Phone", "Tablet", "Headphones", "Smartwatch", "Monitor", "Keyboard", "Mouse"]
months = ["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"]

# Generate 500 expense records
start_date = datetime(2024, 1, 1)
for _ in range(500):
    category = random.choice(expense_categories)
    amount = round(random.uniform(100, 1500), 2)
    date = start_date + timedelta(days=random.randint(0, 730))  # 2 years span
    cursor.execute("INSERT INTO expenses (category, amount, date) VALUES (%s, %s, %s)",
                   (category, amount, date.strftime("%Y-%m-%d")))

# Generate 500 sales records
for _ in range(500):
    product = random.choice(products)
    amount = round(random.uniform(200, 2500), 2)
    month = random.choice(months)
    cursor.execute("INSERT INTO sales (product, amount, month) VALUES (%s, %s, %s)",
                   (product, amount, month))

conn.commit()
cursor.close()
conn.close()

print("Inserted 500 expenses and 500 sales records successfully!")