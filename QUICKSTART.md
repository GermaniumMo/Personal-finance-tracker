"""
Quick Start Guide for Personal Finance Tracker
"""

# WINDOWS SETUP & RUN GUIDE

## 1. Create Virtual Environment

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

## 2. Install Dependencies

```powershell
pip install -r requirements.txt
```

## 3. Create .env File

```powershell
cp .env.example .env
# Edit .env with your SECRET_KEY (generate a random string)
```

## 4. Initialize Database

```powershell
python -c "from app.database import engine, Base; Base.metadata.create_all(bind=engine)"
```

## 5. Run Backend (Terminal 1)

```powershell
uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload
```

**Backend available at:**

- API: http://127.0.0.1:8000
- Swagger Docs: http://127.0.0.1:8000/docs
- ReDoc: http://127.0.0.1:8000/redoc

## 6. Run Frontend (Terminal 2)

```powershell
streamlit run streamlit_app.py
```

**Frontend available at:**

- http://localhost:8501

## 7. Run Tests (Terminal 3)

```powershell
pytest tests/ -v
```

---

## WHAT YOU CAN DO

### Sign Up

1. Go to Streamlit app (http://localhost:8501)
2. Click "Sign Up" tab
3. Enter email, full name, and password (min 8 chars)
4. Account created!

### Login

1. Use email/password from signup
2. JWT token stored in session
3. Access all protected endpoints

### Add Transaction

1. Dashboard → Transactions tab
2. Click "Add Transaction"
3. Enter amount, category, type (income/expense), date
4. Save

### Create Budget

1. Dashboard → Budgets tab
2. Click "Create Budget"
3. Set category limit (e.g., "Food": $500/month)
4. Progress bar updates as you spend

### Set Goal

1. Dashboard → Goals tab
2. Click "Create Goal"
3. Enter name, target amount, deadline
4. Progress circle shows % complete

### View Reports

1. Dashboard → Reports tab
2. See category pie chart
3. Monthly cashflow line chart
4. Download as CSV or JSON

### Manage Settings

1. Dashboard → Settings tab
2. View profile (email)
3. Change theme, currency
4. Logout

---

## API ENDPOINTS (Complete List)

### Authentication

- `POST /auth/signup` - Register new user
- `POST /auth/login` - Get JWT token

### Transactions

- `GET /transactions/` - List transactions
- `POST /transactions/` - Create transaction
- `GET /transactions/{id}` - Get specific transaction
- `PUT /transactions/{id}` - Update transaction
- `DELETE /transactions/{id}` - Delete transaction

### Budgets

- `GET /budgets/` - List budgets
- `POST /budgets/` - Create budget
- `GET /budgets/{id}` - Get specific budget
- `PUT /budgets/{id}` - Update budget
- `DELETE /budgets/{id}` - Delete budget

### Goals

- `GET /goals/` - List goals
- `POST /goals/` - Create goal
- `GET /goals/{id}` - Get specific goal
- `PUT /goals/{id}` - Update goal
- `DELETE /goals/{id}` - Delete goal

### Reports

- `GET /reports/monthly` - Monthly trend
- `GET /reports/category` - Category breakdown
- `GET /reports/summary` - Overall summary
- `GET /reports/budgets` - Budget status
- `GET /reports/goals` - Goals progress

### Health

- `GET /health` - Server health check
- `GET /info` - API info
- `GET /dashboard` - Dashboard summary

---

## EXAMPLE API USAGE (curl)

### Sign Up

```bash
curl -X POST "http://127.0.0.1:8000/auth/signup" \
  -H "Content-Type: application/json" \
  -d '{"email":"user@example.com","full_name":"John Doe","password":"password123"}'
```

### Login

```bash
curl -X POST "http://127.0.0.1:8000/auth/login" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=user@example.com&password=password123"
```

### Create Transaction (with token)

```bash
curl -X POST "http://127.0.0.1:8000/transactions/" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"amount":50,"type":"expense","category":"Food","date":"2025-11-30","method":"card"}'
```

---

## FILE STRUCTURE

```
Personal-finance-tracker/
├── app/
│   ├── __init__.py
│   ├── main.py                 # FastAPI app
│   ├── config.py               # Settings
│   ├── database.py             # SQLAlchemy setup
│   ├── models.py               # ORM models
│   ├── schemas.py              # Pydantic schemas
│   ├── crud.py                 # CRUD operations
│   ├── routers/
│   │   ├── __init__.py
│   │   ├── auth.py             # Auth endpoints
│   │   ├── transactions.py     # Transaction endpoints
│   │   ├── budgets.py          # Budget endpoints
│   │   ├── goals.py            # Goal endpoints
│   │   └── reports.py          # Report endpoints
│   ├── services/
│   │   ├── __init__.py
│   │   ├── reports.py          # Report generation
│   │   └── scraper.py          # Web scraping
│   ├── utils/
│   │   ├── __init__.py
│   │   └── security.py         # Auth utilities
│   └── auth/
│       └── __init__.py
├── database/
│   └── schema.sql              # SQL schema
├── tests/
│   ├── __init__.py
│   ├── conftest.py
│   └── test_main.py            # Pytest tests
├── streamlit_app.py            # Streamlit frontend
├── requirements.txt            # Python dependencies
├── .env.example                # Environment template
├── .gitignore
├── README.md
└── .github/
    └── workflows/
        └── ci.yml              # GitHub Actions CI
```

---

## ENVIRONMENT VARIABLES (.env)

```
DATABASE_URL=sqlite:///./finance.db
SECRET_KEY=generate-a-random-string-here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=10080
DEBUG=True
PROJECT_NAME=Personal Finance Tracker
API_BASE_URL=http://127.0.0.1:8000
```

---

## TROUBLESHOOTING

### "Module not found: app"

- Ensure you're in the project root directory
- Virtual environment is activated

### "Port 8000 in use"

```powershell
# Find and kill process on port 8000
netstat -ano | findstr :8000
taskkill /PID <PID> /F
```

### "Cannot connect to backend from Streamlit"

- Backend running on http://127.0.0.1:8000
- Streamlit on http://localhost:8501
- No HTTPS required for local development

### "Database locked"

- Close Streamlit if tests are running
- Delete `finance.db` and reinitialize

### "Pydantic validation error"

- Check schema in request body matches Pydantic model
- Ensure date format is `YYYY-MM-DD`
- Passwords min 8 characters

---

## PERFORMANCE TIPS

- Limit transactions query: `?limit=100`
- Use date range filter: `/date-range/transactions?start_date=2025-01-01&end_date=2025-12-31`
- Cache dashboard data in Streamlit session
- Use SQLite indexes on frequently queried columns

---

## NEXT STEPS

1. ✅ Backend running
2. ✅ Frontend running
3. → Create test account
4. → Add transactions
5. → Set budgets
6. → Track progress
7. → Export reports
8. → Share with others!

---

Generated: 2025-11-30
Version: 1.0.0
