# 💰 Expense Tracker & Budgeting API

A production-ready REST API for personal finance management built with **FastAPI** and **PostgreSQL**. Track expenses, set monthly budgets, and get smart spending insights with real-time budget vs actual calculations.

---

## 🚀 Features

### 🔐 Authentication & Security
- JWT-based authentication system
- Bcrypt password hashing
- Token-protected routes
- Complete user data isolation

### 💸 Expense Management
- Full CRUD operations for expenses
- Dynamic filtering by category, month, and amount range
- Partial updates (PATCH-like behavior with PUT)
- Date-based queries

### 📁 Category System
- Custom user-defined categories
- Per-user category isolation
- Linked to expenses and budgets via foreign keys

### 💰 Smart Budget Tracking
- Set monthly budgets per category
- Real-time budget vs actual spending calculation
- Automatic budget-exceeded alerts
- Aggregated spending analytics

---

## 🛠️ Tech Stack

| Layer | Technology |
|-------|-----------|
| **Framework** | FastAPI |
| **Database** | PostgreSQL |
| **ORM** | SQLAlchemy |
| **Validation** | Pydantic |
| **Authentication** | JWT (python-jose) |
| **Password Hashing** | Bcrypt (passlib) |
| **Server** | Uvicorn |

---

## 📂 Project Structure

```
expense-tracker-api/
│
├── main.py                  # Application entry point
├── database.py              # Database configuration
├── requirements.txt         # Python dependencies
├── .env                     # Environment variables (not committed)
├── .env.example             # Environment template
│
├── models/                  # SQLAlchemy ORM models
│   ├── user.py
│   ├── category.py
│   ├── expense.py
│   └── budget.py
│
├── schema/                  # Pydantic request/response schemas
│   ├── user.py
│   ├── category.py
│   ├── expense.py
│   └── budget.py
│
├── routes/                  # API endpoints
│   ├── auth.py              # Authentication routes
│   ├── categories.py        # Category CRUD
│   ├── expenses.py          # Expense CRUD + filters
│   └── budgets.py           # Budget management + status
│
└── auth/                    # Authentication utilities
    ├── password.py          # Password hashing
    └── jwt_handler.py       # JWT token logic
```

---

## 🗄️ Database Schema

```
┌─────────────┐       ┌──────────────┐
│   USERS     │       │  CATEGORIES  │
├─────────────┤       ├──────────────┤
│ id (PK)     │──┐    │ id (PK)      │
│ name        │  │    │ name         │
│ email       │  └───<│ user_id (FK) │
│ password    │       │ created_at   │
│ created_at  │       └──────┬───────┘
└──────┬──────┘              │
       │                     │
       │                     │
       │       ┌─────────────┴──┐
       │       │                │
       ▼       ▼                ▼
┌──────────────────┐    ┌─────────────────┐
│    EXPENSES      │    │     BUDGETS     │
├──────────────────┤    ├─────────────────┤
│ id (PK)          │    │ id (PK)         │
│ title            │    │ amount          │
│ amount           │    │ month           │
│ date             │    │ category_id(FK) │
│ note             │    │ user_id (FK)    │
│ category_id (FK) │    │ created_at      │
│ user_id (FK)     │    └─────────────────┘
│ created_at       │
└──────────────────┘
```

### Relationships
- One **User** → Many **Categories**
- One **User** → Many **Expenses**
- One **User** → Many **Budgets**
- One **Category** → Many **Expenses**
- One **Category** → Many **Budgets**

---

## 🔌 API Endpoints

### Authentication

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| POST | `/auth/register` | Register new user | ❌ |
| POST | `/auth/login` | Login and get JWT token | ❌ |
| GET | `/auth/me` | Get current user profile | ✅ |

### Categories

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| POST | `/categories/` | Create category | ✅ |
| GET | `/categories/` | List user's categories | ✅ |
| PUT | `/categories/{id}` | Update category | ✅ |
| DELETE | `/categories/{id}` | Delete category | ✅ |

### Expenses

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| POST | `/expenses/` | Create expense | ✅ |
| GET | `/expenses/` | List expenses (with filters) | ✅ |
| GET | `/expenses/{id}` | Get single expense | ✅ |
| PUT | `/expenses/{id}` | Update expense (partial) | ✅ |
| DELETE | `/expenses/{id}` | Delete expense | ✅ |

#### Available Filters on GET /expenses/
- `?category_id=1` — Filter by category
- `?month=2024-01` — Filter by month
- `?min_amount=100` — Minimum amount
- `?max_amount=500` — Maximum amount
- Can be combined: `?category_id=1&month=2024-01`

### Budgets

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| POST | `/budgets/` | Set budget | ✅ |
| GET | `/budgets/` | List user's budgets | ✅ |
| GET | `/budgets/status?month=2024-01` | Budget vs actual spending | ✅ |

---

## ⚙️ Installation & Setup

### Prerequisites
- Python 3.10+
- PostgreSQL 12+
- pip

### 1. Clone the repository
```bash
git clone https://github.com/yourusername/expense-tracker-api.git
cd expense-tracker-api
```

### 2. Create virtual environment
```bash
python -m venv venv

# Activate (Windows)
venv\Scripts\activate

# Activate (Mac/Linux)
source venv/bin/activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Setup PostgreSQL database
```sql
CREATE DATABASE expensedb;
```

### 5. Configure environment variables
Create a `.env` file:
```bash
DATABASE_URL=postgresql://postgres:yourpassword@localhost:5432/expensedb
SECRET_KEY=your-secret-key-here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

### 6. Run the application
```bash
uvicorn main:app --reload
```

The API will be available at: `http://127.0.0.1:8000`

Interactive docs: `http://127.0.0.1:8000/docs`

---

## 📝 Usage Examples

### Register a User
```bash
POST /auth/register
Content-Type: application/json

{
    "name": "John Doe",
    "email": "john@example.com",
    "password": "securepass123"
}
```

### Login and Get Token
```bash
POST /auth/login
Content-Type: application/json

{
    "email": "john@example.com",
    "password": "securepass123"
}

Response:
{
    "access_token": "eyJhbGciOiJIUzI1...",
    "token_type": "bearer"
}
```

### Create a Category
```bash
POST /categories/
Authorization: Bearer eyJhbGci...
Content-Type: application/json

{
    "name": "Food"
}
```

### Create an Expense
```bash
POST /expenses/
Authorization: Bearer eyJhbGci...

{
    "title": "Lunch at restaurant",
    "amount": 250.00,
    "date": "2024-01-15",
    "note": "Team lunch",
    "category_id": 1
}
```

### Set a Budget
```bash
POST /budgets/
Authorization: Bearer eyJhbGci...

{
    "amount": 5000,
    "month": "2024-01",
    "category_id": 1
}
```

### Check Budget Status
```bash
GET /budgets/status?month=2024-01
Authorization: Bearer eyJhbGci...

Response:
[
    {
        "category": "Food",
        "budget": 5000,
        "spent": 1950,
        "remaining": 3050,
        "is_exceeded": false
    }
]
```

---

## 🔒 Security Features

### Password Security
- All passwords hashed using **bcrypt** with automatic salting
- Plain passwords never stored or logged
- Passwords excluded from all API responses

### Authentication
- **JWT tokens** with configurable expiration
- Bearer token authentication scheme
- Automatic token verification on protected routes

### Data Isolation
- All queries filtered by authenticated user ID
- Users cannot access other users' data
- Foreign key constraints enforce data integrity

### Input Validation
- All inputs validated using **Pydantic schemas**
- Email format validation
- Type checking on all fields
- SQL injection prevention via ORM

---

## 🧠 Key Technical Decisions

### Why FastAPI?
- Modern async support
- Automatic OpenAPI documentation
- Built-in validation
- Production-ready performance

### Why PostgreSQL?
- ACID compliance
- Robust foreign key support
- Industry standard for financial data
- Excellent SQLAlchemy integration

### Why JWT?
- Stateless authentication
- Scalable across multiple servers
- No server-side session storage
- Industry standard for REST APIs

### Why SQLAlchemy ORM?
- Database-agnostic code
- Protection against SQL injection
- Powerful query building
- Migration support ready

---

## 🎯 Business Logic Highlights

### Dynamic Expense Filtering
The expense list endpoint demonstrates query chaining:

```python
query = db.query(Expense).filter(Expense.user_id == user_id)

if category_id:
    query = query.filter(Expense.category_id == category_id)
if month:
    query = query.filter(Expense.date >= start, Expense.date <= end)
if min_amount:
    query = query.filter(Expense.amount >= min_amount)

return query.order_by(Expense.date.desc()).all()
```

### Smart Budget Calculation
The budget status endpoint aggregates expenses against budgets:

1. Fetch all budgets for the specified month
2. For each budget, sum all matching expenses
3. Calculate remaining amount
4. Flag if budget is exceeded
5. Return enriched data with category names

### Partial Updates
Update endpoints use Pydantic's `exclude_unset=True` to update only the fields the user actually sends:

```python
update_data = data.dict(exclude_unset=True)
for field, value in update_data.items():
    setattr(expense, field, value)
```

---

## 🚧 Future Enhancements

- [ ] Recurring expenses support
- [ ] Multi-currency support
- [ ] Export data to CSV/PDF
- [ ] Email notifications for budget alerts
- [ ] Spending analytics dashboard
- [ ] Receipt image upload
- [ ] AI-powered expense categorization
- [ ] Mobile app integration

---

## 🧪 Testing

Test the API interactively using the auto-generated Swagger UI:
```
http://127.0.0.1:8000/docs
```

Or using Postman:
1. Register a user
2. Login to get JWT token
3. Add token to Authorization header (Bearer)
4. Test all endpoints

---

## 📦 Dependencies

```
fastapi
uvicorn
sqlalchemy
psycopg2-binary
python-dotenv
pydantic[email]
python-jose[cryptography]
passlib[bcrypt]
bcrypt==4.0.1
```

---

## 🤝 Contributing

This is a personal learning project, but suggestions and feedback are welcome!

1. Fork the repository
2. Create your feature branch
3. Commit your changes
4. Push to the branch
5. Open a Pull Request

---

## 📜 License

This project is open source and available under the [MIT License](LICENSE).

---

## 👤 Author

**Your Name**
- LinkedIn: [linkedin.com/in/yourprofile](https://linkedin.com)
- GitHub: [github.com/yourusername](https://github.com)
- Email: your.email@example.com

---

## 🙏 Acknowledgments

Built as part of my journey from Python developer to backend engineer. This project taught me:
- Real-world API design patterns
- Database relationships and ORM usage
- Authentication and security best practices
- Production-grade code structure

**Next milestone:** Deployment + AI Integration 🚀

---

⭐ **If this project helped you learn, give it a star!** ⭐

# Additonal Files to Create

.env.example

- Database
DATABASE_URL=postgresql://username:password@localhost:5432/expensedb

- JWT Configuration
SECRET_KEY=your-secret-key-here-change-this
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

.gitignore

- Virtual environment
venv/
env/
ENV/

- Environment variables
.env

- Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
*.egg-info/

- IDE
.vscode/
.idea/
*.swp
*.swo

- OS
.DS_Store
Thumbs.db

- Logs
*.log

# Requirements.txt

- fastapi==0.104.1
- uvicorn==0.24.0
- sqlalchemy==2.0.23
- psycopg2-binary==2.9.9
- python-dotenv==1.0.0
- pydantic[email]==2.5.0
- python-jose[cryptography]==3.3.0
- passlib[bcrypt]==1.7.4
- bcrypt==4.0.1