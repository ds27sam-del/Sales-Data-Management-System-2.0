# Sales & Expense Management System

**A simple, menu-driven CLI application to manage personal or small-business sales and expenses using Python and MySQL.**

---

## 🔧 Features

- Add and view expenses and sales (MySQL-backed)
- Filter expenses by date and sales by product/month
- Top-N summaries (e.g., top 3 expense categories or products)
- Visualizations: expense pie chart, sales bar chart, monthly sales trend
- Scripted sample-data generator (`Data_buddy.py`) to populate the DB for testing

---

## ⚙️ Requirements

- Python 3.10 or newer (required for `match`/`case` usage)
- MySQL server (local or remote)
- Install Python packages:

```bash
python -m venv .venv
# On Windows PowerShell
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

---

## 🗄️ Database setup

1. Create the database (example uses `finance_db`).
2. Import the provided SQL schema and seed data:

```bash
# Import the schema and initial data (adjust user/password as needed)
mysql -u root -p < finance_db.sql
```

3. Confirm connection settings in `app.py` (and `Data_buddy.py` if used):

```python
conn = sql.connect(
    host="localhost",
    user="root",
    password="tiger",
    database="finance_db"
)
```

Change `user`, `password`, `host`, or `database` to match your environment.

---

## ▶️ Running the app

```bash
python app.py
```

- Default demo login: **Sam** / **Sam123**
- Use menu options to add/view/filter data and view charts.

To populate the database with sample data (500 expenses and 500 sales):

```bash
python Data_buddy.py
```

---

## 📌 Notes & Tips

- Visualizations use Matplotlib; on headless servers use `Agg` backend or save charts via `plt.savefig()`.
- For production use, remove hard-coded credentials and adopt environment variables or a secrets manager.
- The project uses `pandas` for simple data handling and `mysql-connector-python` to interact with MySQL.

---

## ✅ Contribution

Feel free to open issues or submit pull requests to improve features, error handling, tests, or add CI.

---

## © License

This project is provided without warranty. Add a license file if you plan to redistribute or publish.
