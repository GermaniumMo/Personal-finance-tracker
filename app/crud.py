from sqlalchemy.orm import Session
from app import models, schemas
from typing import List, Optional, Union
from uuid import UUID, uuid4
from datetime import date, datetime


def create_user(db: Session, user: schemas.UserCreate, hashed_password: str) -> models.User:
    db_user = models.User(
        id=str(uuid4()),
        email=user.email,
        full_name=user.full_name,
        hashed_password=hashed_password,
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_user_by_email(db: Session, email: str) -> Optional[models.User]:
    return db.query(models.User).filter(models.User.email == email).first()


def get_user(db: Session, user_id: str) -> Optional[models.User]:
    return db.query(models.User).filter(models.User.id == user_id).first()


def get_users(db: Session, skip: int = 0, limit: int = 100) -> List[models.User]:
    return db.query(models.User).offset(skip).limit(limit).all()


def update_user(db: Session, user_id: str, user_update: schemas.UserUpdate) -> Optional[models.User]:
    db_user = get_user(db, user_id)
    if not db_user:
        return None
    update_data = user_update.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_user, key, value)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def create_transaction(
    db: Session, user_id: str, transaction: schemas.TransactionCreate
) -> models.Transaction:
    db_transaction = models.Transaction(
        user_id=user_id,
        amount=transaction.amount,
        type=transaction.type,
        category=transaction.category,
        description=transaction.description,
        method=transaction.method,
        date=transaction.date,
    )
    db.add(db_transaction)
    db.commit()
    db.refresh(db_transaction)
    return db_transaction


def get_transactions(
    db: Session, user_id: str, skip: int = 0, limit: int = 100
) -> List[models.Transaction]:
    return (
        db.query(models.Transaction)
        .filter(models.Transaction.user_id == user_id)
        .order_by(models.Transaction.date.desc())
        .offset(skip)
        .limit(limit)
        .all()
    )


def get_transaction(db: Session, user_id: str, transaction_id: int) -> Optional[models.Transaction]:
    return (
        db.query(models.Transaction)
        .filter(models.Transaction.user_id == user_id, models.Transaction.id == transaction_id)
        .first()
    )


def update_transaction(
    db: Session, user_id: str, transaction_id: int, transaction_update: schemas.TransactionUpdate
) -> Optional[models.Transaction]:
    db_transaction = get_transaction(db, user_id, transaction_id)
    if not db_transaction:
        return None
    update_data = transaction_update.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_transaction, key, value)
    db.add(db_transaction)
    db.commit()
    db.refresh(db_transaction)
    return db_transaction


def delete_transaction(db: Session, user_id: str, transaction_id: int) -> bool:
    db_transaction = get_transaction(db, user_id, transaction_id)
    if not db_transaction:
        return False
    db.delete(db_transaction)
    db.commit()
    return True


def get_transactions_by_date_range(
    db: Session, user_id: str, start_date: date, end_date: date
) -> List[models.Transaction]:
    return (
        db.query(models.Transaction)
        .filter(
            models.Transaction.user_id == user_id,
            models.Transaction.date >= start_date,
            models.Transaction.date <= end_date,
        )
        .all()
    )


def create_budget(db: Session, user_id: str, budget: schemas.BudgetCreate) -> models.Budget:
    db_budget = models.Budget(
        user_id=user_id,
        category=budget.category,
        limit_amount=budget.limit_amount,
        period=budget.period,
    )
    db.add(db_budget)
    db.commit()
    db.refresh(db_budget)
    return db_budget


def get_budgets(db: Session, user_id: str) -> List[models.Budget]:
    return db.query(models.Budget).filter(models.Budget.user_id == user_id).all()


def get_budget(db: Session, user_id: str, budget_id: int) -> Optional[models.Budget]:
    return (
        db.query(models.Budget)
        .filter(models.Budget.user_id == user_id, models.Budget.id == budget_id)
        .first()
    )

def update_budget(
    db: Session, user_id: str, budget_id: int, budget_update: schemas.BudgetUpdate
) -> Optional[models.Budget]:
    db_budget = get_budget(db, user_id, budget_id)
    if not db_budget:
        return None
    update_data = budget_update.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_budget, key, value)
    db.add(db_budget)
    db.commit()
    db.refresh(db_budget)
    return db_budget

def delete_budget(db: Session, user_id: str, budget_id: int) -> bool:
    db_budget = get_budget(db, user_id, budget_id)
    if not db_budget:
        return False
    db.delete(db_budget)
    db.commit()
    return True

def create_goal(db: Session, user_id: str, goal: schemas.GoalCreate) -> models.Goal:
    db_goal = models.Goal(
        user_id=user_id,
        name=goal.name,
        target_amount=goal.target_amount,
        current_amount=goal.current_amount,
        deadline=goal.deadline,
    )
    db.add(db_goal)
    db.commit()
    db.refresh(db_goal)
    return db_goal


def get_goals(db: Session, user_id: str) -> List[models.Goal]:
    return db.query(models.Goal).filter(models.Goal.user_id == user_id).all()


def get_goal(db: Session, user_id: str, goal_id: int) -> Optional[models.Goal]:
    return (
        db.query(models.Goal)
        .filter(models.Goal.user_id == user_id, models.Goal.id == goal_id)
        .first()
    )

def update_goal(
    db: Session, user_id: str, goal_id: int, goal_update: schemas.GoalUpdate
) -> Optional[models.Goal]:
    db_goal = get_goal(db, user_id, goal_id)
    if not db_goal:
        return None
    update_data = goal_update.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_goal, key, value)
    if db_goal.current_amount >= db_goal.target_amount:
        db_goal.completed = True
    db.add(db_goal)
    db.commit()
    db.refresh(db_goal)
    return db_goal


def delete_goal(db: Session, user_id: str, goal_id: int) -> bool:
    db_goal = get_goal(db, user_id, goal_id)
    if not db_goal:
        return False
    db.delete(db_goal)
    db.commit()
    return True

def create_notification(
    db: Session, user_id: str, notification: schemas.NotificationCreate
) -> models.Notification:
    db_notification = models.Notification(
        user_id=user_id,
        title=notification.title,
        message=notification.message,
    )
    db.add(db_notification)
    db.commit()
    db.refresh(db_notification)
    return db_notification


def get_notifications(db: Session, user_id: str) -> List[models.Notification]:
    return (
        db.query(models.Notification)
        .filter(models.Notification.user_id == user_id)
        .order_by(models.Notification.created_at.desc())
        .all()
    )


def mark_notification_as_read(db: Session, user_id: str, notification_id: int) -> Optional[models.Notification]:
    db_notification = (
        db.query(models.Notification)
        .filter(models.Notification.user_id == user_id, models.Notification.id == notification_id)
        .first()
    )
    if not db_notification:
        return None
    db_notification.read = True
    db.add(db_notification)
    db.commit()
    db.refresh(db_notification)
    return db_notification
