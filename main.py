from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional
import sqlite3

# -------------------- DB SETUP --------------------
conn = sqlite3.connect("finance.db", check_same_thread=False)
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS transactions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    amount REAL,
    type TEXT,
    category TEXT,
    date TEXT,
    note TEXT
)
""")

conn.commit()

# -------------------- APP --------------------
app = FastAPI()

# -------------------- HOME --------------------
@app.get("/")
def home():
    return {"message": "Backend working"}

# -------------------- MODEL --------------------
class Transaction(BaseModel):
    amount: float
    type: str
    category: str
    date: str
    note: Optional[str] = None

# -------------------- ADD TRANSACTION --------------------
@app.post("/transactions")
def add_transaction(t: Transaction):
    cursor.execute(
        "INSERT INTO transactions (amount, type, category, date, note) VALUES (?, ?, ?, ?, ?)",
        (t.amount, t.type, t.category, t.date, t.note)
    )
    conn.commit()
    return {"message": "Transaction added"}

# -------------------- GET TRANSACTIONS --------------------
@app.get("/transactions")
def get_transactions(type: str = None, category: str = None):
    query = "SELECT * FROM transactions WHERE 1=1"
    params = []

    if type:
        query += " AND LOWER(type) = LOWER(?)"
        params.append(type)

    if category:
        query += " AND LOWER(category) = LOWER(?)"
        params.append(category)

    cursor.execute(query, tuple(params))
    data = cursor.fetchall()

    result = []
    for row in data:
        result.append({
            "id": row[0],
            "amount": row[1],
            "type": row[2],
            "category": row[3],
            "date": row[4],
            "note": row[5]
        })

    return result

@app.get("/transactions/total-income")
def total_income():
    cursor.execute("SELECT SUM(amount) FROM transactions WHERE type = 'income'")
    total = cursor.fetchone()[0]

    return {
        "total_income": total if total else 0
    }

@app.get("/transactions/total-expense")
def total_expense():
    cursor.execute("SELECT SUM(amount) FROM transactions WHERE type = 'expense'")
    total = cursor.fetchone()[0]

    return {
        "total_expense": total if total else 0
    }

@app.get("/transactions/balance")
def balance():
    cursor.execute("SELECT SUM(amount) FROM transactions WHERE type = 'income'")
    income = cursor.fetchone()[0] or 0

    cursor.execute("SELECT SUM(amount) FROM transactions WHERE type = 'expense'")
    expense = cursor.fetchone()[0] or 0

    return {
        "income": income,
        "expense": expense,
        "balance": income - expense
    }


# -------------------- DELETE TRANSACTION --------------------
@app.delete("/transactions/{id}")
def delete_transaction(id: int):
    cursor.execute("DELETE FROM transactions WHERE id = ?", (id,))
    conn.commit()
    return {"message": "Deleted"}

# -------------------- UPDATE TRANSACTION --------------------
@app.put("/transactions/{id}")
def update_transaction(id: int, t: Transaction):
    cursor.execute("""
        UPDATE transactions
        SET amount = ?, type = ?, category = ?, date = ?, note = ?
        WHERE id = ?
    """, (t.amount, t.type, t.category, t.date, t.note, id))

    conn.commit()

    return {"message": "Transaction updated"}