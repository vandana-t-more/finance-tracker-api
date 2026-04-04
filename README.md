# Finance Tracker API
Assignment Submission - Finance Tracker API

A simple and efficient backend API built using FastAPI to manage personal finance transactions like income and expenses.

## Features
-Add transactions (income/expense)
-Get all transactions
-Filter transactions by type and category
-Update transaction details
-Delete transactions
-Calculate:
  Total income
  Total expenses
  Balance

## Tech Stack
-Python
-FastAPI
-SQLite
-Uvicorn
-Pydantic

## Project Structure
finance_backend/
│── main.py
│── requirements.txt
│── .gitignore

## Installation & Setup
1. Clone the repository
git clone https://github.com/vandana-t-more/finance-tracker-api.git
cd finance-tracker-api
2. Install dependencies
pip install -r requirements.txt
3. Run the server
uvicorn main:app --reload

## API Endpoints
Method	Endpoint	Description
POST	/transactions	Add transaction
GET	/transactions	Get all transactions
GET	/transactions/total-income	Get total income
GET	/transactions/total-expense	Get total expense
GET	/transactions/balance	Get balance
PUT	/transactions/{id}	Update transaction
DELETE	/transactions/{id}	Delete transaction

## API Documentation

After running the server, open:

http://127.0.0.1:8000/docs

## Example Request
{
  "amount": 5000,
  "type": "income",
  "category": "salary",
  "date": "2026-04-04",
  "note": "monthly salary"
}
## Future Improvements
User authentication (JWT)
Dashboard & analytics
Monthly reports
Deployment (Render / Railway)
