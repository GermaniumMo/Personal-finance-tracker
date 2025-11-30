import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from datetime import date, timedelta

from app.main import app, get_db
from app.database import Base
from app.utils.security import get_password_hash, verify_password
from app import crud, schemas

SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)


def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)

@pytest.fixture
def test_user_data():
    return {
        "email": "test@example.com",
        "full_name": "Test User",
        "password": "testpassword123",
    }


@pytest.fixture
def create_test_user(test_user_data):
    db = TestingSessionLocal()
    hashed_password = get_password_hash(test_user_data["password"])
    user = crud.create_user(
        db,
        schemas.UserCreate(**test_user_data),
        hashed_password,
    )
    db.close()
    return user

def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_signup_success(test_user_data):
    response = client.post("/auth/signup", json=test_user_data)
    assert response.status_code == 201
    data = response.json()
    assert data["email"] == test_user_data["email"]
    assert data["full_name"] == test_user_data["full_name"]
    assert "id" in data
    assert "password" not in data


def test_signup_duplicate_email(test_user_data):
    client.post("/auth/signup", json=test_user_data)
    response = client.post("/auth/signup", json=test_user_data)
    assert response.status_code == 400
    assert "already registered" in response.json()["detail"]


def test_signup_invalid_email(test_user_data):
    invalid_data = test_user_data.copy()
    invalid_data["email"] = "notanemail"
    response = client.post("/auth/signup", json=invalid_data)
    assert response.status_code == 422


def test_signup_short_password(test_user_data):
    invalid_data = test_user_data.copy()
    invalid_data["password"] = "short"
    response = client.post("/auth/signup", json=invalid_data)
    assert response.status_code == 422


def test_login_success(test_user_data):
    client.post("/auth/signup", json=test_user_data)
    
    response = client.post(
        "/auth/login",
        data={"username": test_user_data["email"], "password": test_user_data["password"]},
    )
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"


def test_login_invalid_email(test_user_data):
    response = client.post(
        "/auth/login",
        data={"username": "nonexistent@example.com", "password": "password123"},
    )
    assert response.status_code == 401


def test_login_invalid_password(test_user_data):
    client.post("/auth/signup", json=test_user_data)
    
    response = client.post(
        "/auth/login",
        data={"username": test_user_data["email"], "password": "wrongpassword"},
    )
    assert response.status_code == 401

def test_password_hash_and_verify():
    password = "mySecurePassword123"
    hashed = get_password_hash(password)
    
    assert hashed != password
    assert "$" in hashed 
    assert verify_password(password, hashed)
    assert not verify_password("wrongpassword", hashed)

def test_get_transactions_unauthenticated():
    """Test getting transactions without authentication."""
    response = client.get("/transactions/")
    assert response.status_code == 403 


def test_create_transaction(test_user_data):
    """Test creating a transaction."""
    # Signup and login
    client.post("/auth/signup", json=test_user_data)
    login_response = client.post(
        "/auth/login",
        data={"username": test_user_data["email"], "password": test_user_data["password"]},
    )
    token = login_response.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}
    
    # Create transaction
    transaction_data = {
        "amount": 50.00,
        "type": "expense",
        "category": "Food",
        "date": str(date.today()),
        "method": "card",
        "description": "Lunch",
    }
    response = client.post("/transactions/", json=transaction_data, headers=headers)
    assert response.status_code == 201
    data = response.json()
    assert data["amount"] == 50.00
    assert data["type"] == "expense"
    assert data["category"] == "Food"


def test_list_transactions(test_user_data):
    """Test listing transactions."""
    # Signup and login
    client.post("/auth/signup", json=test_user_data)
    login_response = client.post(
        "/auth/login",
        data={"username": test_user_data["email"], "password": test_user_data["password"]},
    )
    token = login_response.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}
    
    # Create a transaction
    transaction_data = {
        "amount": 25.50,
        "type": "income",
        "category": "Salary",
        "date": str(date.today()),
        "method": "bank",
    }
    client.post("/transactions/", json=transaction_data, headers=headers)
    
    # List transactions
    response = client.get("/transactions/", headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert len(data) >= 1


def test_update_transaction(test_user_data):
    """Test updating a transaction."""
    # Signup, login, and create transaction
    client.post("/auth/signup", json=test_user_data)
    login_response = client.post(
        "/auth/login",
        data={"username": test_user_data["email"], "password": test_user_data["password"]},
    )
    token = login_response.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}
    
    transaction_data = {
        "amount": 100.00,
        "type": "expense",
        "category": "Entertainment",
        "date": str(date.today()),
        "method": "cash",
    }
    create_response = client.post("/transactions/", json=transaction_data, headers=headers)
    tx_id = create_response.json()["id"]
    
    # Update transaction
    update_data = {"amount": 75.00, "category": "Food"}
    response = client.put(f"/transactions/{tx_id}", json=update_data, headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert data["amount"] == 75.00
    assert data["category"] == "Food"


def test_delete_transaction(test_user_data):
    """Test deleting a transaction."""
    # Signup, login, and create transaction
    client.post("/auth/signup", json=test_user_data)
    login_response = client.post(
        "/auth/login",
        data={"username": test_user_data["email"], "password": test_user_data["password"]},
    )
    token = login_response.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}
    
    transaction_data = {
        "amount": 50.00,
        "type": "expense",
        "category": "Food",
        "date": str(date.today()),
    }
    create_response = client.post("/transactions/", json=transaction_data, headers=headers)
    tx_id = create_response.json()["id"]
    
    # Delete transaction
    response = client.delete(f"/transactions/{tx_id}", headers=headers)
    assert response.status_code == 204


# ============= Budget Tests =============


def test_create_budget(test_user_data):
    """Test creating a budget."""
    client.post("/auth/signup", json=test_user_data)
    login_response = client.post(
        "/auth/login",
        data={"username": test_user_data["email"], "password": test_user_data["password"]},
    )
    token = login_response.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}
    
    budget_data = {
        "category": "Food",
        "limit_amount": 500.00,
        "period": "monthly",
    }
    response = client.post("/budgets/", json=budget_data, headers=headers)
    assert response.status_code == 201
    data = response.json()
    assert data["category"] == "Food"
    assert data["limit_amount"] == 500.00


def test_list_budgets(test_user_data):
    """Test listing budgets."""
    client.post("/auth/signup", json=test_user_data)
    login_response = client.post(
        "/auth/login",
        data={"username": test_user_data["email"], "password": test_user_data["password"]},
    )
    token = login_response.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}
    
    # Create budget
    budget_data = {"category": "Transport", "limit_amount": 200.00}
    client.post("/budgets/", json=budget_data, headers=headers)
    
    # List
    response = client.get("/budgets/", headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert len(data) >= 1


# ============= Goal Tests =============


def test_create_goal(test_user_data):
    """Test creating a goal."""
    client.post("/auth/signup", json=test_user_data)
    login_response = client.post(
        "/auth/login",
        data={"username": test_user_data["email"], "password": test_user_data["password"]},
    )
    token = login_response.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}
    
    goal_data = {
        "name": "Vacation Fund",
        "target_amount": 5000.00,
        "current_amount": 1000.00,
        "deadline": str(date.today() + timedelta(days=365)),
    }
    response = client.post("/goals/", json=goal_data, headers=headers)
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "Vacation Fund"
    assert data["target_amount"] == 5000.00


def test_list_goals(test_user_data):
    """Test listing goals."""
    client.post("/auth/signup", json=test_user_data)
    login_response = client.post(
        "/auth/login",
        data={"username": test_user_data["email"], "password": test_user_data["password"]},
    )
    token = login_response.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}
    
    # Create goal
    goal_data = {
        "name": "Emergency Fund",
        "target_amount": 10000.00,
        "deadline": str(date.today() + timedelta(days=730)),
    }
    client.post("/goals/", json=goal_data, headers=headers)
    
    # List
    response = client.get("/goals/", headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert len(data) >= 1


# ============= Reports Tests =============


def test_get_monthly_report(test_user_data):
    """Test getting monthly report."""
    client.post("/auth/signup", json=test_user_data)
    login_response = client.post(
        "/auth/login",
        data={"username": test_user_data["email"], "password": test_user_data["password"]},
    )
    token = login_response.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}
    
    response = client.get("/reports/monthly", headers=headers)
    assert response.status_code == 200


def test_get_category_report(test_user_data):
    """Test getting category breakdown report."""
    client.post("/auth/signup", json=test_user_data)
    login_response = client.post(
        "/auth/login",
        data={"username": test_user_data["email"], "password": test_user_data["password"]},
    )
    token = login_response.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}
    
    response = client.get("/reports/category", headers=headers)
    assert response.status_code == 200
