"""Budgets router for CRUD operations."""

from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import Annotated, List

from app import crud, schemas, models
from app.database import get_db
from app.routers.auth import get_current_user

router = APIRouter(prefix="/budgets", tags=["Budgets"])


@router.post("/", response_model=schemas.BudgetOut, status_code=201)
def create_budget(
    budget: schemas.BudgetCreate,
    current_user: Annotated[models.User, Depends(get_current_user)],
    db: Session = Depends(get_db),
):
    return crud.create_budget(db, current_user.id, budget)


@router.get("/", response_model=List[schemas.BudgetOut])
def list_budgets(
    current_user: Annotated[models.User, Depends(get_current_user)],
    db: Session = Depends(get_db),
):
    return crud.get_budgets(db, current_user.id)


@router.get("/{budget_id}", response_model=schemas.BudgetOut)
def get_budget(
    budget_id: int,
    current_user: Annotated[models.User, Depends(get_current_user)],
    db: Session = Depends(get_db),
):
    budget = crud.get_budget(db, current_user.id, budget_id)
    if not budget:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Budget not found")
    return budget


@router.put("/{budget_id}", response_model=schemas.BudgetOut)
def update_budget(
    budget_id: int,
    budget_update: schemas.BudgetUpdate,
    current_user: Annotated[models.User, Depends(get_current_user)],
    db: Session = Depends(get_db),
):
    budget = crud.update_budget(db, current_user.id, budget_id, budget_update)
    if not budget:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Budget not found")
    return budget


@router.delete("/{budget_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_budget(
    budget_id: int,
    current_user: Annotated[models.User, Depends(get_current_user)],
    db: Session = Depends(get_db),
):
    success = crud.delete_budget(db, current_user.id, budget_id)
    if not success:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Budget not found")
