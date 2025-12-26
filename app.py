# -------------------------------
# Sales & Expense Management System v2.2
# Author: Saumya Kumar
# Description:
#   Menu-driven Python + MySQL app to manage expenses and sales,
#   with filtering and Matplotlib visualizations.
# -------------------------------

import mysql.connector as sql
import matplotlib.pyplot as plt
import pandas as pd
from datetime import datetime
from typing import Optional
import maskpass

# Establish MySQL connection (ensure finance_db exists)
conn = sql.connect(
    host="localhost",
    user="root",
    password="tiger",
    database="finance_db"
)
cur = conn.cursor()

# -------------------------------
# Application entry
# -------------------------------
def main():
    """
    Entry point: handles login and shows menu.
    Each menu option routes to a function with proper user inputs.
    """
    login = {"Sam": "Sam123"}  # simple credential store

    user = input("Enter the name of user: ").strip()
    password = maskpass.askpass(prompt="Enter your password: ", mask="*").strip()

    # Correct login check
    if user in login and password == login[user]:
        print(f"Welcome, {user}!")
        while True:
            print(
                "\n----- What do you want to do -----\n"
                " 1. Add data in table expense\n"
                " 2. Add data in table sales\n"
                " 3. See the data of table expense\n"
                " 4. See the data of table sales\n"
                " 5. Filter the data of table expense (by date range)\n"
                " 6. Filter the data of table sales (by product/month)\n"
                " 7. Top 3 expense categories\n"
                " 8. Top 3 sales products\n"
                " 9. Expense pie chart\n"
                " 10. Sales bar chart\n"
                " 11. Sales trend line\n"
                " 12. Exit"
            )
            try:
                choice = int(input("Enter choice: ").strip())
            except ValueError:
                print("Please enter a valid number.")
                continue

            match choice:
                case 1:
                    # Prompt inputs for expense insertion
                    category = input("Category: ").strip()
                    try:
                        amount = float(input("Amount: ").strip())
                    except ValueError:
                        print("Amount must be a number.")
                        continue
                    date_str = input("Date (YYYY-MM-DD): ").strip()
                    add_expense(category, amount, date_str)

                case 2:
                    # Prompt inputs for sales insertion
                    product = input("Product: ").strip()
                    try:
                        amount = float(input("Amount: ").strip())
                    except ValueError:
                        print("Amount must be a number.")
                        continue
                    month = input("Month (e.g., Jan): ").strip()
                    add_sales(product, amount, month)

                case 3:
                    view_expenses()

                case 4:
                    view_sales()

                case 5:
                    start_date = input("Start date (YYYY-MM-DD): ").strip()
                    end_date = input("End date (YYYY-MM-DD): ").strip()
                    filter_expenses_by_date_range(start_date, end_date)

                case 6:
                    product = input("Product (leave blank for any): ").strip() or None
                    month = input("Month (e.g., Jan) (leave blank for any): ").strip() or None
                    filter_sales(product=product, month=month)

                case 7:
                    print(top_expense_categories(3))

                case 8:
                    print(top_sales_products(3))

                case 9:
                    expense_pie_chart()

                case 10:
                    sales_bar_chart()

                case 11:
                    sales_trend_line()

                case 12:
                    print("Thank you. Goodbye!")
                    break

                case _:
                    print("Invalid choice. Try again.")
    else:
        print("Invalid login. Try Again!")
        main()  # retry login

# -------------------------------
# Database operations
# -------------------------------
def add_expense(category: str, amount: float, date_str: str):
    """Insert a new expense record into the database."""
    try:
        _ = datetime.strptime(date_str, "%Y-%m-%d")  # validate date format
    except ValueError:
        print("Invalid date format. Use YYYY-MM-DD.")
        return

    cur.execute(
        "INSERT INTO expenses (category, amount, date) VALUES (%s, %s, %s)",
        (category, amount, date_str)
    )
    conn.commit()
    print("Expense added.")

def add_sales(product: str, amount: float, month: str):
    """Insert a new sales record into the database."""
    cur.execute(
        "INSERT INTO sales (product, amount, month) VALUES (%s, %s, %s)",
        (product, amount, month)
    )
    conn.commit()  # missing before; now fixed
    print("Sale added.")

def df_expenses() -> pd.DataFrame:
    """Return all expenses as a Pandas DataFrame."""
    return pd.read_sql(
        "SELECT id, category, amount, date FROM expenses ORDER BY date ASC",
        conn
    )

def df_sales() -> pd.DataFrame:
    """Return all sales as a Pandas DataFrame."""
    return pd.read_sql(
        "SELECT id, product, amount, month FROM sales ORDER BY id ASC",
        conn
    )

def view_expenses():
    """Display all expenses in tabular format."""
    df = df_expenses()
    print(df if not df.empty else "No expenses found.")

def view_sales():
    """Display all sales in tabular format."""
    df = df_sales()
    print(df if not df.empty else "No sales found.")

def filter_expenses_by_date_range(start_date: str, end_date: str):
    """Filter expenses between two dates (inclusive)."""
    try:
        _ = datetime.strptime(start_date, "%Y-%m-%d")
        _ = datetime.strptime(end_date, "%Y-%m-%d")
    except ValueError:
        print("Invalid date format. Use YYYY-MM-DD.")
        return

    query = """
        SELECT category, amount, date
        FROM expenses
        WHERE date BETWEEN %s AND %s
        ORDER BY date ASC;
    """
    df = pd.read_sql(query, conn, params=(start_date, end_date))
    print(df if not df.empty else "No expenses in the provided date range.")
    return df

def filter_sales(product: Optional[str] = None, month: Optional[str] = None):
    """Filter sales by product and/or month."""
    base = "SELECT product, amount, month FROM sales WHERE 1=1"
    params = []
    if product:
        base += " AND product = %s"
        params.append(product)
    if month:
        base += " AND month = %s"
        params.append(month)

    df = pd.read_sql(base, conn, params=params if params else None)
    print(df if not df.empty else "No sales for given filters.")
    return df

def top_expense_categories(top_n: int = 3) -> pd.DataFrame:
    """Return top N expense categories by total amount."""
    df = pd.read_sql(
        "SELECT category, SUM(amount) AS total FROM expenses GROUP BY category ORDER BY total DESC",
        conn
    )
    return df.head(top_n)

def top_sales_products(top_n: int = 3) -> pd.DataFrame:
    """Return top N sales products by total amount."""
    df = pd.read_sql(
        "SELECT product, SUM(amount) AS total FROM sales GROUP BY product ORDER BY total DESC",
        conn
    )
    return df.head(top_n)

# -------------------------------
# Visualization
# -------------------------------
def expense_pie_chart():
    """Generate a pie chart of expenses by category."""
    df = pd.read_sql(
        "SELECT category, SUM(amount) AS total FROM expenses GROUP BY category",
        conn
    )
    if df.empty:
        print("No expenses to visualize.")
        return

    plt.figure(figsize=(8, 6))
    plt.pie(df["total"], labels=df["category"], autopct="%1.1f%%", startangle=140)
    plt.title("Expense Distribution by Category")
    plt.show()

def sales_bar_chart():
    """Generate a bar chart of sales by product."""
    df = pd.read_sql(
        "SELECT product, SUM(amount) AS total FROM sales GROUP BY product ORDER BY total DESC",
        conn
    )
    if df.empty:
        print("No sales to visualize.")
        return

    plt.figure(figsize=(9, 6))
    plt.bar(df["product"], df["total"], color="skyblue")
    plt.title("Sales by Product")
    plt.xlabel("Product")
    plt.ylabel("Total Sales")
    plt.xticks(rotation=30, ha="right")
    plt.show()

def sales_trend_line():
    """Generate a line chart of monthly sales trend."""
    df = pd.read_sql(
        "SELECT month, SUM(amount) AS total FROM sales GROUP BY month",
        conn
    )
    if df.empty:
        print("No sales to visualize.")
        return

    # Sort months in calendar order if short names are used
    order = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
    df["month_index"] = df["month"].apply(lambda m: order.index(m) if m in order else 99)
    df = df.sort_values("month_index")

    plt.figure(figsize=(9, 6))
    plt.plot(df["month"], df["total"], marker="o")
    plt.title("Monthly Sales Trend")
    plt.xlabel("Month")
    plt.ylabel("Total Sales")
    plt.show()

# -------------------------------
# Run Application
# -------------------------------
if __name__ == "__main__":
    main()