from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import Annotated, Dict, List

from app import models, schemas
from app.database import get_db
from app.routers.auth import get_current_user
from app.services.reports import ReportGenerator

router = APIRouter(prefix="/reports", tags=["Reports"])


@router.get("/monthly", response_model=Dict[str, Dict[str, float]])
def get_monthly_report(
    current_user: Annotated[models.User, Depends(get_current_user)],
    db: Session = Depends(get_db),
):
    generator = ReportGenerator(db, current_user.id)
    return generator.monthly_trend()


@router.get("/category", response_model=Dict[str, float])
def get_category_report(
    current_user: Annotated[models.User, Depends(get_current_user)],
    db: Session = Depends(get_db),
):
    generator = ReportGenerator(db, current_user.id)
    return generator.category_summary()


@router.get("/summary")
def get_summary(
    current_user: Annotated[models.User, Depends(get_current_user)],
    db: Session = Depends(get_db),
):
    generator = ReportGenerator(db, current_user.id)
    return {
        "income_vs_expenses": generator.income_vs_expenses(),
        "category_breakdown": generator.category_summary(),
        "budget_status": generator.budget_status(),
        "goals": generator.goal_progress(),
    }


@router.get("/budgets")
def get_budget_report(
    current_user: Annotated[models.User, Depends(get_current_user)],
    db: Session = Depends(get_db),
):
    generator = ReportGenerator(db, current_user.id)
    return generator.budget_status()


@router.get("/goals")
def get_goals_report(
    current_user: Annotated[models.User, Depends(get_current_user)],
    db: Session = Depends(get_db),
):
    generator = ReportGenerator(db, current_user.id)
    return generator.goal_progress()
