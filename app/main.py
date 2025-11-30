from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

from app.database import engine, Base, get_db
from app.routers import auth, transactions, budgets, goals, reports
from app.models import User
from app.schemas import DashboardSummary
from app.services.reports import ReportGenerator
from app.config import settings
from app import crud

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title=settings.PROJECT_NAME,
    description="A full-stack personal finance tracker with budget and goal management.",
    version="1.0.0",
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(transactions.router)
app.include_router(budgets.router)
app.include_router(goals.router)
app.include_router(reports.router)

@app.get("/health")
def health_check():
    return {"status": "ok"}


@app.get("/info")
def info():
    return {
        "name": settings.PROJECT_NAME,
        "version": "1.0.0",
        "docs": "/docs",
        "openapi": "/openapi.json",
    }


@app.get("/dashboard", response_model=DashboardSummary)
def get_dashboard(
    current_user: User = Depends(auth.get_current_user),
    db: Session = Depends(get_db),
):
    generator = ReportGenerator(db, current_user.id)
    transactions = generator.get_transactions()
    
    total_income = sum(tx.amount for tx in transactions if tx.type == "income")
    total_expenses = sum(tx.amount for tx in transactions if tx.type == "expense")
    net_balance = total_income - total_expenses
    
    budgets = crud.get_budgets(db, current_user.id)
    goals = crud.get_goals(db, current_user.id)
    
    return DashboardSummary(
        total_income=total_income,
        total_expenses=total_expenses,
        net_balance=net_balance,
        transaction_count=len(transactions),
        budget_count=len(budgets),
        goal_count=len(goals),
    )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
