# 💰 Expense Tracker & Budgeting API

Production-ready REST API for personal finance management built with FastAPI and PostgreSQL.

## 🚀 Features

- **JWT Authentication** with bcrypt password hashing
- **Expense Management** with dynamic filtering (category, month, amount)
- **Custom Categories** per user
- **Smart Budget Tracking** with real-time vs actual calculations
- **Budget Alerts** when limits are exceeded
- **Full User Data Isolation** for security

## 🛠️ Tech Stack

- **Backend:** FastAPI
- **Database:** PostgreSQL
- **ORM:** SQLAlchemy
- **Authentication:** JWT (python-jose)
- **Validation:** Pydantic
- **Password Hashing:** bcrypt

## 📂 Project Structure

```
expense-tracker-api/
├── main.py
├── database.py
├── models/      # SQLAlchemy models
├── schema/      # Pydantic schemas
├── routes/      # API endpoints
└── auth/        # Auth utilities
```

## ⚙️ Setup

```bash
# Clone
git clone https://github.com/dc-singh/expense-tracker-api.git
cd expense-tracker-api

# Virtual environment
python -m venv venv
venv\Scripts\activate  # Windows
source venv/bin/activate  # Mac/Linux

# Install dependencies
pip install -r requirements.txt

# Setup .env
cp .env.example .env
# Add your database URL and secret key

# Run
uvicorn main:app --reload
```

API available at: `http://127.0.0.1:8000`

Docs at: `http://127.0.0.1:8000/docs`

## 🔌 API Endpoints

### Authentication
- `POST /auth/register` - Register new user
- `POST /auth/login` - Login and get JWT
- `GET /auth/me` - Get current user

### Categories
- `POST /categories/` - Create category
- `GET /categories/` - List categories
- `PUT /categories/{id}` - Update category
- `DELETE /categories/{id}` - Delete category

### Expenses
- `POST /expenses/` - Create expense
- `GET /expenses/` - List with filters
- `GET /expenses/{id}` - Get single expense
- `PUT /expenses/{id}` - Update expense
- `DELETE /expenses/{id}` - Delete expense

#### Available Filters
- `?category_id=1`
- `?month=2024-01`
- `?min_amount=100&max_amount=500`

### Budgets
- `POST /budgets/` - Set budget
- `GET /budgets/` - List budgets
- `GET /budgets/status?month=2024-01` - Smart budget vs actual

## 🔐 Security

- Bcrypt password hashing
- JWT token authentication
- User data isolation on every query
- Pydantic input validation
- SQL injection prevention via ORM

## 📝 License

MIT