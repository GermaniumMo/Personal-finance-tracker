from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import Annotated, List

from app import crud, schemas, models
from app.database import get_db
from app.routers.auth import get_current_user

router = APIRouter(prefix="/goals", tags=["Goals"])


@router.post("/", response_model=schemas.GoalOut, status_code=201)
def create_goal(
    goal: schemas.GoalCreate,
    current_user: Annotated[models.User, Depends(get_current_user)],
    db: Session = Depends(get_db),
):
    return crud.create_goal(db, current_user.id, goal)


@router.get("/", response_model=List[schemas.GoalOut])
def list_goals(
    current_user: Annotated[models.User, Depends(get_current_user)],
    db: Session = Depends(get_db),
):
    return crud.get_goals(db, current_user.id)


@router.get("/{goal_id}", response_model=schemas.GoalOut)
def get_goal(
    goal_id: int,
    current_user: Annotated[models.User, Depends(get_current_user)],
    db: Session = Depends(get_db),
):
    goal = crud.get_goal(db, current_user.id, goal_id)
    if not goal:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Goal not found")
    return goal


@router.put("/{goal_id}", response_model=schemas.GoalOut)
def update_goal(
    goal_id: int,
    goal_update: schemas.GoalUpdate,
    current_user: Annotated[models.User, Depends(get_current_user)],
    db: Session = Depends(get_db),
):
    goal = crud.update_goal(db, current_user.id, goal_id, goal_update)
    if not goal:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Goal not found")
    return goal


@router.delete("/{goal_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_goal(
    goal_id: int,
    current_user: Annotated[models.User, Depends(get_current_user)],
    db: Session = Depends(get_db),
):
    success = crud.delete_goal(db, current_user.id, goal_id)
    if not success:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Goal not found")
