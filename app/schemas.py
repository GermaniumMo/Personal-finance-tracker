from pydantic import BaseModel, EmailStr, Field, validator
from typing import Optional, List
from datetime import datetime, date

class UserBase(BaseModel):

    email: EmailStr
    full_name: str = Field(..., min_length=1, max_length=255)


class UserCreate(UserBase):

    password: str = Field(..., min_length=8, max_length=100)


class UserUpdate(BaseModel):

    full_name: Optional[str] = Field(None, max_length=255)
    currency: Optional[str] = Field(None, max_length=3)


class UserOut(UserBase):

    id: str
    role: str
    currency: str
    created_at: datetime

    class Config:
        from_attributes = True

class TransactionBase(BaseModel):

    amount: float = Field(..., gt=0)
    type: str = Field(..., pattern="^(income|expense)$")
    category: str = Field(..., min_length=1, max_length=100)
    description: Optional[str] = Field(None, max_length=500)
    method: str = Field(default="cash", max_length=100)
    date: date


class TransactionCreate(TransactionBase):

    pass


class TransactionUpdate(BaseModel):

    amount: Optional[float] = Field(None, gt=0)
    type: Optional[str] = Field(None, pattern="^(income|expense)$")
    category: Optional[str] = Field(None, min_length=1, max_length=100)
    description: Optional[str] = Field(None, max_length=500)
    method: Optional[str] = Field(None, max_length=100)
    date: Optional[date] = None


class TransactionOut(TransactionBase):

    id: int
    user_id: str
    created_at: datetime

    class Config:
        from_attributes = True

class BudgetBase(BaseModel):

    category: str = Field(..., min_length=1, max_length=100)
    limit_amount: float = Field(..., gt=0)
    period: str = Field(default="monthly", pattern="^(monthly|yearly|weekly)$")


class BudgetCreate(BudgetBase):
    pass


class BudgetUpdate(BaseModel):

    category: Optional[str] = Field(None, max_length=100)
    limit_amount: Optional[float] = Field(None, gt=0)
    period: Optional[str] = None


class BudgetOut(BudgetBase):

    id: int
    user_id: str
    created_at: datetime

    class Config:
        from_attributes = True

class GoalBase(BaseModel):

    name: str = Field(..., min_length=1, max_length=255)
    target_amount: float = Field(..., gt=0)
    current_amount: float = Field(default=0.0, ge=0)
    deadline: date


class GoalCreate(GoalBase):

    pass


class GoalUpdate(BaseModel):

    name: Optional[str] = Field(None, max_length=255)
    target_amount: Optional[float] = Field(None, gt=0)
    current_amount: Optional[float] = Field(None, ge=0)
    deadline: Optional[date] = None


class GoalOut(GoalBase):

    id: int
    user_id: str
    completed: bool
    created_at: datetime

    class Config:
        from_attributes = True


class NotificationBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=255)
    message: str = Field(..., min_length=1, max_length=1000)


class NotificationCreate(NotificationBase):

    pass


class NotificationOut(NotificationBase):

    id: int
    user_id: str
    read: bool
    created_at: datetime

    class Config:
        from_attributes = True

class Token(BaseModel):

    access_token: str
    token_type: str = "bearer"


class TokenData(BaseModel):

    user_id: str
    role: str

class DashboardSummary(BaseModel):

    total_income: float
    total_expenses: float
    net_balance: float
    transaction_count: int
    budget_count: int
    goal_count: int


class CategoryBreakdown(BaseModel):

    category: str
    amount: float
    percentage: float


class MonthlyTrend(BaseModel):

    month: str
    income: float
    expenses: float
    net: float


class ReportData(BaseModel):

    monthly_trends: List[MonthlyTrend]
    category_breakdown: List[CategoryBreakdown]
    total_income: float
    total_expenses: float
