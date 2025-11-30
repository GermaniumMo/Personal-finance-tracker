import streamlit as st
import requests
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta, date
from typing import Optional, Dict, List
import json
from pathlib import Path

API_BASE = "http://127.0.0.1:8000"
THEME_COLORS = {
    "primary": "#2962FF", 
    "success": "#2ECC71", 
    "danger": "#E74C3C", 
    "warning": "#F39C12",
    "secondary": "#7E57C2",
}

st.set_page_config(
    page_title="Personal Finance Tracker",
    page_icon="💰",
    layout="wide",
    initial_sidebar_state="expanded",
)

def initialize_session_state():
    if "token" not in st.session_state:
        st.session_state.token = None
    if "user" not in st.session_state:
        st.session_state.user = None
    if "theme" not in st.session_state:
        st.session_state.theme = "light"


initialize_session_state()


def api_request(method: str, endpoint: str, data: Optional[Dict] = None, authenticated: bool = True) -> Optional[Dict]:
    headers = {}
    if authenticated and st.session_state.token:
        headers["Authorization"] = f"Bearer {st.session_state.token}"
    
    try:
        url = f"{API_BASE}{endpoint}"
        if method == "GET":
            response = requests.get(url, headers=headers, timeout=10)
        elif method == "POST":
            response = requests.post(url, json=data, headers=headers, timeout=10)
        elif method == "PUT":
            response = requests.put(url, json=data, headers=headers, timeout=10)
        elif method == "DELETE":
            response = requests.delete(url, headers=headers, timeout=10)
        
        response.raise_for_status()
        return response.json() if response.text else None
    except requests.exceptions.RequestException as e:
        st.error(f"API Error: {str(e)}")
        return None

def login_page():
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.title("💰 Personal Finance Tracker")
        st.markdown("---")
        
        tab1, tab2 = st.tabs(["Login", "Sign Up"])
        
        with tab1:
            st.subheader("Login")
            email = st.text_input("Email", key="login_email")
            password = st.text_input("Password", type="password", key="login_password")
            
            if st.button("Login", use_container_width=True):
                if not email or not password:
                    st.error("Please fill in all fields")
                else:
                    try:
                        response = requests.post(
                            f"{API_BASE}/auth/login",
                            data={"username": email, "password": password},
                            timeout=10,
                        )
                        if response.status_code == 200:
                            data = response.json()
                            st.session_state.token = data["access_token"]
                            st.session_state.user = email
                            st.success("Logged in successfully!")
                            st.rerun()
                        else:
                            st.error("Invalid email or password")
                    except Exception as e:
                        st.error(f"Login failed: {str(e)}")
        
        with tab2:
            st.subheader("Create Account")
            name = st.text_input("Full Name", key="signup_name")
            email = st.text_input("Email", key="signup_email")
            password = st.text_input("Password (min 8 chars)", type="password", key="signup_password")
            password_confirm = st.text_input("Confirm Password", type="password", key="signup_confirm")
            
            if st.button("Sign Up", use_container_width=True):
                if not all([name, email, password, password_confirm]):
                    st.error("Please fill in all fields")
                elif len(password) < 8:
                    st.error("Password must be at least 8 characters")
                elif password != password_confirm:
                    st.error("Passwords do not match")
                else:
                    try:
                        response = requests.post(
                            f"{API_BASE}/auth/signup",
                            json={
                                "email": email,
                                "full_name": name,
                                "password": password,
                            },
                            timeout=10,
                        )
                        if response.status_code == 201:
                            st.success("Account created! Please login.")
                            st.session_state.clear()
                            st.rerun()
                        else:
                            st.error(f"Signup failed: {response.json().get('detail', 'Unknown error')}")
                    except Exception as e:
                        st.error(f"Signup failed: {str(e)}")

def dashboard_page():
    st.title("📊 Dashboard")
    
    dashboard_data = api_request("GET", "/dashboard")
    if not dashboard_data:
        st.error("Failed to load dashboard data")
        return
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("💵 Total Income", f"${dashboard_data['total_income']:.2f}")
    with col2:
        st.metric("💸 Total Expenses", f"${dashboard_data['total_expenses']:.2f}")
    with col3:
        net = dashboard_data["total_income"] - dashboard_data["total_expenses"]
        st.metric("📈 Net Balance", f"${net:.2f}", delta=f"${net:.2f}")
    with col4:
        st.metric("📝 Transactions", dashboard_data["transaction_count"])
    
    st.markdown("---")

    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Spending by Category")
        categories = api_request("GET", "/reports/category")
        if categories:
            fig = go.Figure(data=[go.Pie(labels=list(categories.keys()), values=list(categories.values()))])
            fig.update_traces(hoverinfo="label+percent+value", textposition="auto")
            st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.subheader("Monthly Trend")
        monthly = api_request("GET", "/reports/monthly")
        if monthly:
            df = pd.DataFrame([
                {"Month": month, "Income": data["income"], "Expenses": data["expenses"]}
                for month, data in monthly.items()
            ])
            fig = px.line(df, x="Month", y=["Income", "Expenses"], markers=True)
            st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("---")
    
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("📋 Recent Transactions")
        transactions = api_request("GET", "/transactions/?limit=5")
        if transactions:
            df = pd.DataFrame(transactions)
            st.dataframe(df[["date", "category", "type", "amount"]], use_container_width=True)
    
    with col2:
        st.subheader("🎯 Goals Progress")
        goals = api_request("GET", "/reports/goals")
        if goals:
            for goal_name, goal_data in goals.items():
                st.write(f"**{goal_name}**")
                st.progress(goal_data["percentage"] / 100)
                st.write(f"${goal_data['current']:.2f} / ${goal_data['target']:.2f}")

def transactions_page():
    st.title("💳 Transactions")
    
    tab1, tab2 = st.tabs(["View Transactions", "Add Transaction"])
    
    with tab1:
        col1, col2, col3 = st.columns(3)
        with col1:
            category_filter = st.selectbox("Filter by Category", ["All", "Food", "Transport", "Entertainment", "Utilities", "Other"])
        with col2:
            type_filter = st.selectbox("Filter by Type", ["All", "income", "expense"])
        with col3:
            sort_order = st.selectbox("Sort by Date", ["Newest First", "Oldest First"])
        
        transactions = api_request("GET", "/transactions/?limit=1000")
        if transactions:
            df = pd.DataFrame(transactions)
            if category_filter != "All":
                df = df[df["category"] == category_filter]
            if type_filter != "All":
                df = df[df["type"] == type_filter]

            df = df.sort_values("date", ascending=(sort_order == "Oldest First"))
            
            st.dataframe(
                df[["date", "category", "type", "amount", "description"]],
                use_container_width=True,
            )
    
    with tab2:
        st.subheader("Add New Transaction")
        col1, col2 = st.columns(2)
        
        with col1:
            amount = st.number_input("Amount", min_value=0.01, step=0.01)
            tx_type = st.selectbox("Type", ["expense", "income"])
            category = st.selectbox("Category", ["Food", "Transport", "Entertainment", "Utilities", "Salary", "Other"])
        
        with col2:
            tx_date = st.date_input("Date", value=date.today())
            method = st.selectbox("Payment Method", ["cash", "card", "bank"])
            description = st.text_input("Description")
        
        if st.button("Add Transaction", use_container_width=True):
            result = api_request("POST", "/transactions/", {
                "amount": amount,
                "type": tx_type,
                "category": category,
                "date": tx_date.isoformat(),
                "method": method,
                "description": description,
            })
            if result:
                st.success("Transaction added!")
                st.rerun()

def budgets_page():
    st.title("💰 Budgets")
    
    tab1, tab2 = st.tabs(["View Budgets", "Create Budget"])
    
    with tab1:
        budgets_data = api_request("GET", "/reports/budgets")
        if budgets_data:
            for category, budget_info in budgets_data.items():
                with st.container():
                    col1, col2, col3 = st.columns([2, 1, 1])
                    with col1:
                        st.write(f"**{category}**")
                        st.progress(budget_info["percentage"] / 100)
                    with col2:
                        st.write(f"Spent: ${budget_info['spent']:.2f}")
                    with col3:
                        st.write(f"Limit: ${budget_info['limit']:.2f}")
    
    with tab2:
        st.subheader("Create New Budget")
        col1, col2 = st.columns(2)
        
        with col1:
            category = st.text_input("Category")
            limit_amount = st.number_input("Monthly Limit", min_value=0.01, step=0.01)
        
        with col2:
            period = st.selectbox("Period", ["monthly", "yearly"])
        
        if st.button("Create Budget", use_container_width=True):
            result = api_request("POST", "/budgets/", {
                "category": category,
                "limit_amount": limit_amount,
                "period": period,
            })
            if result:
                st.success("Budget created!")
                st.rerun()

def goals_page():
    st.title("🎯 Goals")
    
    tab1, tab2 = st.tabs(["View Goals", "Create Goal"])
    
    with tab1:
        goals_data = api_request("GET", "/reports/goals")
        if goals_data:
            for goal_name, goal_info in goals_data.items():
                with st.container():
                    col1, col2, col3 = st.columns([2, 1, 1])
                    with col1:
                        st.write(f"**{goal_name}**")
                        st.progress(goal_info["percentage"] / 100)
                    with col2:
                        st.write(f"Saved: ${goal_info['current']:.2f}")
                    with col3:
                        st.write(f"Target: ${goal_info['target']:.2f}")
    
    with tab2:
        st.subheader("Create New Goal")
        col1, col2 = st.columns(2)
        
        with col1:
            name = st.text_input("Goal Name")
            target_amount = st.number_input("Target Amount", min_value=0.01, step=0.01)
        
        with col2:
            deadline = st.date_input("Deadline")
            current_amount = st.number_input("Current Savings", min_value=0.0, step=0.01)
        
        if st.button("Create Goal", use_container_width=True):
            result = api_request("POST", "/goals/", {
                "name": name,
                "target_amount": target_amount,
                "current_amount": current_amount,
                "deadline": deadline.isoformat(),
            })
            if result:
                st.success("Goal created!")
                st.rerun()

def reports_page():
    st.title("📈 Reports")
    
    tab1, tab2 = st.tabs(["Charts", "Export"])
    
    with tab1:
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Category Breakdown")
            categories = api_request("GET", "/reports/category")
            if categories:
                fig = px.bar(
                    x=list(categories.keys()),
                    y=list(categories.values()),
                    labels={"x": "Category", "y": "Amount ($)"},
                )
                st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.subheader("Monthly Cashflow")
            monthly = api_request("GET", "/reports/monthly")
            if monthly:
                df = pd.DataFrame([
                    {"Month": month, "Income": data["income"], "Expenses": data["expenses"], "Net": data["income"] - data["expenses"]}
                    for month, data in monthly.items()
                ])
                fig = px.line(df, x="Month", y=["Income", "Expenses", "Net"], markers=True)
                st.plotly_chart(fig, use_container_width=True)
    
    with tab2:
        st.subheader("Export Data")
        transactions = api_request("GET", "/transactions/?limit=10000")
        if transactions:
            df = pd.DataFrame(transactions)
            
            col1, col2 = st.columns(2)
            with col1:
                csv = df.to_csv(index=False)
                st.download_button(
                    label="Download CSV",
                    data=csv,
                    file_name=f"transactions_{date.today()}.csv",
                    mime="text/csv",
                )
            
            with col2:
                json_data = df.to_json(orient="records")
                st.download_button(
                    label="Download JSON",
                    data=json_data,
                    file_name=f"transactions_{date.today()}.json",
                    mime="application/json",
                )

def settings_page():
    st.title("⚙️ Settings")
    
    tab1, tab2, tab3 = st.tabs(["Profile", "Preferences", "Help"])
    
    with tab1:
        st.subheader("Profile")
        st.write(f"**Email:** {st.session_state.user}")
        if st.button("Logout", use_container_width=True):
            st.session_state.token = None
            st.session_state.user = None
            st.success("Logged out!")
            st.rerun()
    
    with tab2:
        st.subheader("Preferences")
        theme = st.selectbox("Theme", ["Light", "Dark"])
        currency = st.selectbox("Currency", ["USD", "EUR", "GBP", "JPY", "CAD", "AUD"])
        st.write(f"Selected: {theme} theme, {currency}")
    
    with tab3:
        st.subheader("Help & Support")
        st.write("**FAQ:**")
        st.write("- Q: How do I add a transaction? A: Go to Transactions tab and use 'Add Transaction' form.")
        st.write("- Q: How do I create a budget? A: Go to Budgets tab and set a monthly limit per category.")
        st.write("- Q: How do I export data? A: Go to Reports tab and download CSV or JSON.")

def main():
    if not st.session_state.token:
        login_page()
    else:
        with st.sidebar:
            st.title("💰 Finance Tracker")
            st.write(f"Welcome, {st.session_state.user}!")
            st.markdown("---")
            
            page = st.radio(
                "Navigation",
                ["Dashboard", "Transactions", "Budgets", "Goals", "Reports", "Settings"],
                key="page_radio",
            )
        
        if page == "Dashboard":
            dashboard_page()
        elif page == "Transactions":
            transactions_page()
        elif page == "Budgets":
            budgets_page()
        elif page == "Goals":
            goals_page()
        elif page == "Reports":
            reports_page()
        elif page == "Settings":
            settings_page()


if __name__ == "__main__":
    main()
