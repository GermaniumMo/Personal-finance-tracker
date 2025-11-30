from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import Annotated, List
from datetime import date

from app import crud, schemas, models
from app.database import get_db
from app.routers.auth import get_current_user

router = APIRouter(prefix="/transactions", tags=["Transactions"])


@router.post("/", response_model=schemas.TransactionOut, status_code=201)
def create_transaction(
    transaction: schemas.TransactionCreate,
    current_user: Annotated[models.User, Depends(get_current_user)],
    db: Session = Depends(get_db),
):
    return crud.create_transaction(db, current_user.id, transaction)


@router.get("/", response_model=List[schemas.TransactionOut])
def list_transactions(
    current_user: Annotated[models.User, Depends(get_current_user)],
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    db: Session = Depends(get_db),
):
    return crud.get_transactions(db, current_user.id, skip, limit)


@router.get("/{transaction_id}", response_model=schemas.TransactionOut)
def get_transaction(
    transaction_id: int,
    current_user: Annotated[models.User, Depends(get_current_user)],
    db: Session = Depends(get_db),
):
    transaction = crud.get_transaction(db, current_user.id, transaction_id)
    if not transaction:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Transaction not found")
    return transaction


@router.put("/{transaction_id}", response_model=schemas.TransactionOut)
def update_transaction(
    transaction_id: int,
    transaction_update: schemas.TransactionUpdate,
    current_user: Annotated[models.User, Depends(get_current_user)],
    db: Session = Depends(get_db),
):
    transaction = crud.update_transaction(db, current_user.id, transaction_id, transaction_update)
    if not transaction:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Transaction not found")
    return transaction


@router.delete("/{transaction_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_transaction(
    transaction_id: int,
    current_user: Annotated[models.User, Depends(get_current_user)],
    db: Session = Depends(get_db),
):
    success = crud.delete_transaction(db, current_user.id, transaction_id)
    if not success:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Transaction not found")


@router.get("/date-range/transactions", response_model=List[schemas.TransactionOut])
def get_transactions_by_date(
    start_date: date,
    end_date: date,
    current_user: Annotated[models.User, Depends(get_current_user)],
    db: Session = Depends(get_db),
):
    """Get transactions within a date range."""
    return crud.get_transactions_by_date_range(db, current_user.id, start_date, end_date)
