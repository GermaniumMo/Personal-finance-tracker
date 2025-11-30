from sqlalchemy.orm import Session
from typing import List, Dict
from datetime import datetime, timedelta
from collections import defaultdict

from app import models, crud


class ReportGenerator:

    def __init__(self, db: Session, user_id: str):
        self.db = db
        self.user_id = user_id

    def get_transactions(self) -> List:
        return crud.get_transactions(self.db, self.user_id, skip=0, limit=10000)

    def category_summary(self) -> Dict[str, float]:
        transactions = self.get_transactions()
        summary = defaultdict(float)
        
        for tx in transactions:
            if tx.type == "expense":
                summary[tx.category] += tx.amount
        
        return dict(summary)

    def monthly_trend(self) -> Dict[str, Dict[str, float]]:
        transactions = self.get_transactions()
        trend = defaultdict(lambda: {"income": 0.0, "expenses": 0.0})
        
        for tx in transactions:
            month_key = tx.date.strftime("%Y-%m")
            if tx.type == "income":
                trend[month_key]["income"] += tx.amount
            else:
                trend[month_key]["expenses"] += tx.amount
        
        return dict(trend)

    def income_vs_expenses(self) -> Dict[str, float]:
        transactions = self.get_transactions()
        total_income = sum(tx.amount for tx in transactions if tx.type == "income")
        total_expenses = sum(tx.amount for tx in transactions if tx.type == "expense")
        
        return {
            "income": total_income,
            "expenses": total_expenses,
            "net": total_income - total_expenses,
        }

    def budget_status(self) -> Dict[str, Dict]:
        budgets = crud.get_budgets(self.db, self.user_id)
        transactions = self.get_transactions()
        
        budget_status = {}
        for budget in budgets:
            spent = sum(tx.amount for tx in transactions if tx.category == budget.category and tx.type == "expense")
            percentage = (spent / budget.limit_amount * 100) if budget.limit_amount > 0 else 0
            budget_status[budget.category] = {
                "limit": budget.limit_amount,
                "spent": spent,
                "remaining": max(0, budget.limit_amount - spent),
                "percentage": min(100, percentage),
            }
        
        return budget_status

    def goal_progress(self) -> Dict[str, Dict]:
        goals = crud.get_goals(self.db, self.user_id)
        goal_progress = {}
        
        for goal in goals:
            percentage = (goal.current_amount / goal.target_amount * 100) if goal.target_amount > 0 else 0
            days_left = (goal.deadline - datetime.now().date()).days if goal.deadline else 0
            goal_progress[goal.name] = {
                "target": goal.target_amount,
                "current": goal.current_amount,
                "percentage": min(100, percentage),
                "completed": goal.completed,
                "days_left": max(0, days_left),
            }
        
        return goal_progress
