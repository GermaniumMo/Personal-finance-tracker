# Personal Finance Tracker

A full-stack web application for tracking income, expenses, budgets, and financial goals.

## Tech Stack

**Backend:** FastAPI + SQLAlchemy + SQLite  
**Frontend:** Streamlit  
**Authentication:** OAuth2 + JWT (PBKDF2 hashing)  
**Data Viz:** Plotly + Matplotlib  
**Web Scraping:** BeautifulSoup + html5lib + lxml

## Features

- User authentication (signup/login with JWT tokens)
- Transaction management (add/edit/delete income and expenses)
- Budget tracking with category limits and progress visualization
- Goal setting with progress circles and deadlines
- Reports: monthly trends, category breakdowns, income vs. expenses
- Dark/Light theme toggle
- Responsive dashboard with charts and analytics
- Role-based access control

## Project Structure

```
/app
  /routers           # API route handlers
  /services          # Business logic (reports, scraping)
  /auth              # Authentication & security
  /utils             # Helpers & utilities
  models.py          # SQLAlchemy models
  schemas.py         # Pydantic validation schemas
  crud.py            # Database operations
  database.py        # DB connection & session
  config.py          # Settings
  main.py            # FastAPI app

/database
  schema.sql         # Initial SQLite schema

/tests               # Pytest test files

streamlit_app.py     # Streamlit frontend entry point
requirements.txt     # Python dependencies
.env.example         # Environment variables template
README.md            # This file
```

## Setup

### 1. Create Virtual Environment

```bash
python -m venv .venv
.venv\Scripts\activate  # Windows
# or
source .venv/bin/activate  # macOS/Linux
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Create .env File

```bash
cp .env.example .env
# Edit .env with your SECRET_KEY and other settings
```

### 4. Initialize Database

```bash
python -c "from app.database import engine, Base; Base.metadata.create_all(bind=engine)"
```

### 5. Run Backend

```bash
uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload
```

Backend available at: http://127.0.0.1:8000  
API docs at: http://127.0.0.1:8000/docs

### 6. Run Frontend (in new terminal)

```bash
streamlit run streamlit_app.py
```

Frontend available at: http://localhost:8501

## Testing

```bash
pytest tests/ -v
```

## Troubleshooting

**pandas build error on Windows:**

- Use conda: `conda install pandas`
- Or install pre-built wheel: `pip install pandas --only-binary :all:`

**passlib/bcrypt issues:**

- This project uses PBKDF2-HMAC-SHA256 instead of bcrypt; no native compilation required.

**Port already in use:**

- Backend: `uvicorn app.main:app --port 8001`
- Frontend: `streamlit run streamlit_app.py --server.port 8502`

## API Endpoints

**Auth**

- `POST /auth/signup` - Register new user
- `POST /auth/login` - Login and get JWT token

**Transactions**

- `GET /transactions/` - List user transactions
- `POST /transactions/` - Create transaction
- `PUT /transactions/{id}` - Update transaction
- `DELETE /transactions/{id}` - Delete transaction

**Budgets**

- `GET /budgets/` - List budgets
- `POST /budgets/` - Create budget
- `PUT /budgets/{id}` - Update budget
- `DELETE /budgets/{id}` - Delete budget

**Goals**

- `GET /goals/` - List goals
- `POST /goals/` - Create goal
- `PUT /goals/{id}` - Update goal
- `DELETE /goals/{id}` - Delete goal

**Reports**

- `GET /reports/monthly` - Monthly spending trend
- `GET /reports/category` - Spending by category

## Architecture

### Backend (FastAPI)

- **Models:** SQLAlchemy ORM with relationships
- **Schemas:** Pydantic v2 validation
- **CRUD:** Repository pattern for data access
- **Auth:** OAuth2 + JWT with PBKDF2-HMAC-SHA256 hashing
- **Services:** Business logic (reports, scraping)
- **Routers:** RESTful endpoints with dependency injection

### Frontend (Streamlit)

- **Multi-page:** Dashboard, Transactions, Budgets, Goals, Reports, Settings
- **Auth:** Session-based token management
- **Charts:** Plotly + Matplotlib for visualizations
- **Theme:** Light/Dark toggle support
- **Export:** CSV and JSON download

### Database (SQLite)

- Users with role-based access
- Transactions with categories and methods
- Budgets with spending limits
- Goals with progress tracking
- Notifications system

## Project Features

✅ User authentication (signup/login)
✅ JWT token-based authorization
✅ CRUD operations for transactions, budgets, goals
✅ Role-based access control (user/admin)
✅ Financial reporting and analytics
✅ Interactive dashboards with charts
✅ Web scraping utilities
✅ Data export (CSV/JSON)
✅ Comprehensive test suite
✅ Type hints throughout
✅ Error handling and validation
✅ CORS-enabled API
✅ API documentation (Swagger UI)

## API Design System

**Colors:** Primary Blue (#2962FF), Success Green (#2ECC71), Danger Red (#E74C3C)  
**Typography:** Inter/Roboto, H1 32px, Body 14-16px  
**Components:** 16px border radius, soft shadows, floating labels

## Technology Stack Details

| Component        | Technology                        |
| ---------------- | --------------------------------- |
| Backend          | FastAPI 0.104.1                   |
| Web Server       | Uvicorn 0.24.0                    |
| ORM              | SQLAlchemy 2.0.23                 |
| Validation       | Pydantic 2.5.0                    |
| Auth             | Python-Jose 3.3.0                 |
| Password Hashing | PBKDF2-HMAC-SHA256 (built-in)     |
| Frontend         | Streamlit 1.28.1                  |
| Data Analysis    | Pandas 2.1.3                      |
| Visualizations   | Plotly 5.17.0, Matplotlib 3.8.2   |
| Web Scraping     | BeautifulSoup4 4.12.2, lxml 4.9.3 |
| Testing          | Pytest 7.4.3                      |
| Migrations       | Alembic 1.13.0                    |

## Contributing

1. Fork the repo
2. Create a feature branch: `git checkout -b feature/your-feature`
3. Run tests: `pytest tests/ -v`
4. Commit changes: `git commit -m 'Add your feature'`
5. Push to branch: `git push origin feature/your-feature`
6. Open a Pull Request

## Common Issues & Solutions

**Port Already in Use (Backend):**

```bash
# Use a different port
uvicorn app.main:app --port 8001
```

**Port Already in Use (Frontend):**

```bash
# Streamlit will auto-increment, or specify:
streamlit run streamlit_app.py --server.port 8502
```

**CORS Errors:**

- Ensure backend is running on http://127.0.0.1:8000
- Streamlit runs on http://localhost:8501

**Database Issues:**

- Delete `finance.db` to reset
- Create fresh tables with: `python -c "from app.database import engine, Base; Base.metadata.create_all(bind=engine)"`

**Authentication Problems:**

- Check `.env` SECRET_KEY is set
- Verify token not expired (default 7 days)
- Ensure email/password are correct

## Performance Tips

- Index on frequently queried fields (user_id, date, category)
- Pagination on list endpoints (limit=100)
- Cache dashboard data client-side
- Use connection pooling for database

## Security Checklist

- [ ] Change SECRET_KEY in production
- [ ] Set DEBUG=False
- [ ] Use HTTPS in production
- [ ] Validate all inputs (Pydantic handles this)
- [ ] Use strong passwords (min 8 chars)
- [ ] Rotate JWT tokens periodically
- [ ] Use environment variables for secrets
- [ ] Implement rate limiting

## Future Enhancements

- [ ] Recurring transactions
- [ ] Savings automation
- [ ] Bill reminders
- [ ] Multi-currency support
- [ ] Mobile app (React Native)
- [ ] Advanced analytics (ML/predictions)
- [ ] Bank integration (Plaid API)
- [ ] Investment tracking
- [ ] Tax reporting
- [ ] Backup & restore functionality

## License

MIT

## Support

For issues or questions, please open an issue on GitHub or contact the maintainers.
