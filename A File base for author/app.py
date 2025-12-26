import pandas as pd
import matplotlib.pyplot as plt

# Load data
expenses = pd.read_csv('expenses.csv')
sales = pd.read_csv('sales.csv')

# Expense Analysis
expense_totals = expenses.groupby('Category')['Amount'].sum().sort_values(ascending=False)

# Sales Analysis
sales_totals = sales.groupby('Product')['Amount'].sum().sort_values(ascending=False)
monthly_sales = sales.groupby('Month')['Amount'].sum()

# Expense Pie Chart
plt.figure(figsize=(8,6))
plt.pie(expense_totals, labels=expense_totals.index, autopct='%1.1f%%', startangle=140)
plt.title('Expense Distribution by Category')
plt.savefig('expense_chart.png')
plt.show()

# Sales Bar Chart
plt.figure(figsize=(8,6))
sales_totals.plot(kind='bar', color='skyblue')
plt.title('Sales by Product')
plt.xlabel('Product')
plt.ylabel('Total Sales')
plt.savefig('sales_chart.png')
plt.show()

# Sales Trend Line Chart
plt.figure(figsize=(8,6))
monthly_sales.plot(kind='line', marker='o')
plt.title('Monthly Sales Trend')
plt.xlabel('Month')
plt.ylabel('Sales Amount')
plt.savefig('sales_trend.png')
plt.show()