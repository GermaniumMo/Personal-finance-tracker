from sqlalchemy import Column, String, Integer, Float, DateTime, Boolean, ForeignKey, Date
from sqlalchemy.orm import relationship
from datetime import datetime
import uuid

from app.database import Base


class User(Base):

    __tablename__ = "users"

    id: str = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    email: str = Column(String(255), unique=True, nullable=False, index=True)
    full_name: str = Column(String(255), nullable=False)
    hashed_password: str = Column(String(255), nullable=False)
    role: str = Column(String(50), default="user")
    currency: str = Column(String(3), default="USD")
    created_at: datetime = Column(DateTime, default=datetime.utcnow)
    transactions = relationship("Transaction", back_populates="user", cascade="all, delete-orphan")
    budgets = relationship("Budget", back_populates="user", cascade="all, delete-orphan")
    goals = relationship("Goal", back_populates="user", cascade="all, delete-orphan")
    notifications = relationship("Notification", back_populates="user", cascade="all, delete-orphan")


class Transaction(Base):

    __tablename__ = "transactions"

    id: int = Column(Integer, primary_key=True, autoincrement=True)
    user_id: str = Column(String(36), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    amount: float = Column(Float, nullable=False)
    type: str = Column(String(50), nullable=False) 
    category: str = Column(String(100), nullable=False)
    description: str = Column(String(500))
    method: str = Column(String(100), default="cash") 
    date: str = Column(Date, nullable=False, index=True)
    created_at: datetime = Column(DateTime, default=datetime.utcnow)
    user = relationship("User", back_populates="transactions")


class Budget(Base):

    __tablename__ = "budgets"

    id: int = Column(Integer, primary_key=True, autoincrement=True)
    user_id: str = Column(String(36), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    category: str = Column(String(100), nullable=False)
    limit_amount: float = Column(Float, nullable=False)
    period: str = Column(String(50), default="monthly")
    created_at: datetime = Column(DateTime, default=datetime.utcnow)
    user = relationship("User", back_populates="budgets")


class Goal(Base):

    __tablename__ = "goals"

    id: int = Column(Integer, primary_key=True, autoincrement=True)
    user_id: str = Column(String(36), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    name: str = Column(String(255), nullable=False)
    target_amount: float = Column(Float, nullable=False)
    current_amount: float = Column(Float, default=0.0)
    deadline: str = Column(Date, nullable=False)
    completed: bool = Column(Boolean, default=False)
    created_at: datetime = Column(DateTime, default=datetime.utcnow)
    user = relationship("User", back_populates="goals")


class Notification(Base):

    __tablename__ = "notifications"

    id: int = Column(Integer, primary_key=True, autoincrement=True)
    user_id: str = Column(String(36), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    title: str = Column(String(255), nullable=False)
    message: str = Column(String(1000), nullable=False)
    read: bool = Column(Boolean, default=False)
    created_at: datetime = Column(DateTime, default=datetime.utcnow)
    user = relationship("User", back_populates="notifications")
