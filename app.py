"""
app.py
------
Interactive Streamlit Financial Analytics & Expense Tracker Dashboard.
Provides real-time interactive filters, KPI metrics, dynamic charts,
budget rule auditing, anomaly detection, manual expense entry, and data export.
"""

import os
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime

from src.analytics import (
    compute_financial_kpis,
    get_category_breakdown,
    get_monthly_trends,
    evaluate_50_30_20_rule,
    detect_overspending_and_anomalies,
    generate_automated_insights
)
from src.data_preprocessing import clean_and_preprocess_data, classify_budget_bucket
from src.generate_data import generate_synthetic_expenses

# Page Configuration
st.set_page_config(
    page_title="FinTrack - Expense Analytics Dashboard",
    page_icon="💳",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Styling
st.markdown("""
<style>
    .metric-card {
        background-color: #f8f9fa;
        border-radius: 10px;
        padding: 15px;
        border-left: 5px solid #4b7bec;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
    }
    .kpi-title { font-size: 0.9rem; color: #6c757d; font-weight: 600; margin-bottom: 5px; }
    .kpi-value { font-size: 1.8rem; font-weight: 700; color: #2d3436; }
</style>
""", unsafe_allow_html=True)

@st.cache_data
def load_data():
    csv_path = "data/cleaned_expenses.csv"
    if not os.path.exists(csv_path):
        if not os.path.exists("data/raw_expenses.csv"):
            generate_synthetic_expenses()
        clean_and_preprocess_data()
    df = pd.read_csv(csv_path)
    df["Date"] = pd.to_datetime(df["Date"])
    return df

# Initialize data
df = load_data()

# ==========================================
# SIDEBAR CONTROLS & FILTERS
# ==========================================
st.sidebar.image("https://img.icons8.com/isometric/100/wallet.png", width=80)
st.sidebar.title("FinTrack Controls")
st.sidebar.markdown("Personal Finance & Business Spend Analytics")

# Add Transaction Form (Virtual simulation / Interactive input)
with st.sidebar.expander("➕ Log New Transaction", expanded=False):
    with st.form("new_txn_form", clear_on_submit=True):
        new_date = st.date_input("Date", value=datetime.today())
        new_type = st.selectbox("Type", ["Expense", "Income"])
        new_cat = st.selectbox("Category", [
            "Food & Dining", "Groceries", "Rent & Housing", "Bills & Utilities",
            "Transportation", "Entertainment", "Shopping", "Health & Fitness",
            "Subscriptions", "Salary", "Freelance & Side Income", "Other"
        ])
        new_desc = st.text_input("Description", value="Manual Entry")
        new_amount = st.number_input("Amount (₹)", min_value=1.0, value=500.0, step=50.0)
        new_pay_method = st.selectbox("Payment Method", ["UPI", "Credit Card", "Debit Card", "Net Banking", "Cash"])
        
        submitted = st.form_submit_button("Submit Transaction")
        if submitted:
            new_record = pd.DataFrame([{
                "Transaction_ID": f"TXN{len(df)+1001}",
                "Date": pd.to_datetime(new_date),
                "Category": new_cat.strip().title(),
                "Description": new_desc.strip(),
                "Amount": float(new_amount),
                "Type": new_type,
                "Payment_Method": new_pay_method,
                "Year": new_date.year,
                "Month_Num": new_date.month,
                "Month_Name": new_date.strftime("%B"),
                "Year_Month": new_date.strftime("%Y-%m"),
                "Day": new_date.day,
                "Weekday": new_date.strftime("%A"),
                "Is_Weekend": new_date.weekday() in [5, 6],
                "Quarter": f"Q{(new_date.month-1)//3 + 1}",
                "Budget_Bucket": classify_budget_bucket({"Type": new_type, "Category": new_cat})
            }])
            df = pd.concat([df, new_record], ignore_index=True)
            df.to_csv("data/cleaned_expenses.csv", index=False)
            st.sidebar.success("Transaction added!")
            st.rerun()

st.sidebar.markdown("---")
st.sidebar.subheader("🔍 Filter Records")

# Category filter
available_categories = sorted(df["Category"].unique())
selected_categories = st.sidebar.multiselect(
    "Expense / Income Category",
    options=available_categories,
    default=available_categories
)

# Transaction Type filter
selected_type = st.sidebar.radio("Transaction Type", ["All", "Expense", "Income"], horizontal=True)

# Payment method filter
available_pay_methods = sorted(df["Payment_Method"].unique())
selected_methods = st.sidebar.multiselect(
    "Payment Rail",
    options=available_pay_methods,
    default=available_pay_methods
)

# Date filter
min_date = df["Date"].min().date()
max_date = df["Date"].max().date()
date_range = st.sidebar.date_input(
    "Date Window",
    value=(min_date, max_date),
    min_value=min_date,
    max_value=max_date
)

# Apply filters
filtered_df = df[df["Category"].isin(selected_categories)]
filtered_df = filtered_df[filtered_df["Payment_Method"].isin(selected_methods)]

if selected_type != "All":
    filtered_df = filtered_df[filtered_df["Type"] == selected_type]

if isinstance(date_range, (tuple, list)) and len(date_range) == 2:
    filtered_df = filtered_df[
        (filtered_df["Date"].dt.date >= date_range[0]) & 
        (filtered_df["Date"].dt.date <= date_range[1])
    ]

# ==========================================
# MAIN DASHBOARD VIEW
# ==========================================
st.title("💳 Expense Tracker & Financial Intelligence Dashboard")
st.markdown("A data-driven analytics platform for tracking personal or corporate cash flow, budget leak detection, and behavioral spending insights.")

# Executive KPIs
kpis = compute_financial_kpis(filtered_df)

col1, col2, col3, col4, col5 = st.columns(5)
with col1:
    st.metric("Total Inflow", f"₹{kpis['total_income']:,.0f}", delta=f"{kpis['num_income_txns']} Credits")
with col2:
    st.metric("Total Outflow", f"₹{kpis['total_expense']:,.0f}", delta=f"-{kpis['num_expense_txns']} Debits", delta_color="inverse")
with col3:
    st.metric("Net Savings", f"₹{kpis['net_savings']:,.0f}", delta=f"{kpis['savings_rate_pct']}% of Income")
with col4:
    st.metric("Avg Monthly Expense", f"₹{kpis['avg_monthly_expense']:,.0f}")
with col5:
    st.metric("Daily Burn Rate", f"₹{kpis['daily_burn_rate']:,.0f}/day")

st.markdown("---")

# Navigation Tabs
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "📈 Spending Trends",
    "🍕 Category Breakdown",
    "🎯 50/30/20 Budget Health",
    "⚠️ Outliers & Patterns",
    "📄 Data Explorer & Report"
])

# ------------------------------------------
# TAB 1: SPENDING TRENDS
# ------------------------------------------
with tab1:
    st.subheader("Monthly Income vs. Outflow Trajectory")
    monthly_data = get_monthly_trends(filtered_df)
    
    if not monthly_data.empty:
        fig, ax = plt.subplots(figsize=(12, 4.5))
        x = np.arange(len(monthly_data))
        w = 0.35
        
        ax.bar(x - w/2, monthly_data["Income"], w, label="Inflow (Income)", color="#2ecc71")
        ax.bar(x + w/2, monthly_data["Expense"], w, label="Outflow (Expense)", color="#e74c3c")
        ax.plot(x, monthly_data["Net_Savings"], color="#3498db", marker="o", linewidth=2.5, label="Net Savings")
        
        ax.set_xticks(x)
        ax.set_xticklabels(monthly_data["Year_Month"], rotation=30, ha="right")
        ax.set_ylabel("Amount (₹)")
        ax.yaxis.set_major_formatter('₹{x:,.0f}')
        ax.legend()
        ax.grid(axis='y', linestyle='--', alpha=0.5)
        st.pyplot(fig)
        
        st.markdown("#### Monthly Performance Summary Table")
        display_monthly = monthly_data[["Year_Month", "Income", "Expense", "Net_Savings", "Savings_Rate_Pct", "Expense_MoM_Growth_Pct"]].copy()
        display_monthly.columns = ["Month", "Inflow (₹)", "Outflow (₹)", "Net Savings (₹)", "Savings Rate (%)", "Expense MoM Growth (%)"]
        st.dataframe(display_monthly.style.format({
            "Inflow (₹)": "₹{:,.2f}",
            "Outflow (₹)": "₹{:,.2f}",
            "Net Savings (₹)": "₹{:,.2f}",
            "Savings Rate (%)": "{:.2f}%",
            "Expense MoM Growth (%)": "{:.2f}%"
        }), use_container_width=True)
    else:
        st.info("No transaction data available for selected filter window.")

# ------------------------------------------
# TAB 2: CATEGORY BREAKDOWN
# ------------------------------------------
with tab2:
    st.subheader("Expense Distribution by Category")
    cat_df = get_category_breakdown(filtered_df)
    
    if not cat_df.empty:
        c1, c2 = st.columns([1.2, 1])
        
        with c1:
            fig, ax = plt.subplots(figsize=(8, 5))
            sns.barplot(data=cat_df, x="Total_Spend", y="Category", palette="mako", ax=ax)
            ax.set_xlabel("Total Amount (₹)")
            ax.xaxis.set_major_formatter('₹{x:,.0f}')
            ax.set_title("Expenditure per Category")
            for p in ax.patches:
                width = p.get_width()
                ax.annotate(f"₹{width:,.0f}", (width, p.get_y() + p.get_height() / 2.),
                            ha='left', va='center', xytext=(5, 0), textcoords='offset points', fontsize=9)
            st.pyplot(fig)
            
        with c2:
            fig, ax = plt.subplots(figsize=(6, 5))
            ax.pie(cat_df["Total_Spend"], labels=cat_df["Category"], autopct="%1.1f%%",
                   colors=sns.color_palette("Set2", len(cat_df)), startangle=140,
                   wedgeprops=dict(width=0.4, edgecolor='white'))
            ax.set_title("Proportion of Total Spend")
            st.pyplot(fig)
            
        st.dataframe(cat_df.style.format({
            "Total_Spend": "₹{:,.2f}",
            "Avg_Ticket_Size": "₹{:,.2f}",
            "Percentage_Share": "{:.2f}%"
        }), use_container_width=True)
    else:
        st.info("No expense categories found in current filter.")

# ------------------------------------------
# TAB 3: 50/30/20 BUDGET HEALTH
# ------------------------------------------
with tab3:
    st.subheader("Personal Finance Health Check: 50/30/20 Rule")
    st.markdown("""
    The **50/30/20 Rule** is an industry standard budgeting model:
    - **50% Needs**: Essential living expenses (Rent, Utilities, Basic Groceries, Healthcare)
    - **30% Wants**: Discretionary lifestyle choices (Dining out, Entertainment, Shopping, Streaming)
    - **20% Savings / Investments**: Retained wealth and emergency fund building
    """)
    
    budget_stats = evaluate_50_30_20_rule(filtered_df)
    if "error" not in budget_stats:
        b1, b2, b3 = st.columns(3)
        with b1:
            st.metric("Needs Allocation", f"{budget_stats['needs_pct']}%", delta="Target: ≤ 50%",
                      delta_color="normal" if budget_stats['needs_compliant'] else "inverse")
        with b2:
            st.metric("Wants Allocation", f"{budget_stats['wants_pct']}%", delta="Target: ≤ 30%",
                      delta_color="normal" if budget_stats['wants_compliant'] else "inverse")
        with b3:
            st.metric("Savings Allocation", f"{budget_stats['savings_pct']}%", delta="Target: ≥ 20%",
                      delta_color="normal" if budget_stats['savings_compliant'] else "inverse")
            
        fig, ax = plt.subplots(figsize=(8, 3.5))
        categories = ["Needs", "Wants", "Savings"]
        target = [50.0, 30.0, 20.0]
        actual = [budget_stats["needs_pct"], budget_stats["wants_pct"], budget_stats["savings_pct"]]
        
        x = np.arange(len(categories))
        w = 0.35
        ax.bar(x - w/2, target, w, label="Target Benchmark %", color="#bdc3c7")
        ax.bar(x + w/2, actual, w, label="Actual Spending %", color=["#3498db", "#e67e22", "#2ecc71"])
        ax.set_xticks(x)
        ax.set_xticklabels(categories, fontsize=11, weight="bold")
        ax.set_ylabel("Share of Inflow (%)")
        ax.legend()
        for i in range(len(categories)):
            ax.text(x[i] - w/2, target[i] + 1, f"{target[i]}%", ha="center", fontsize=9)
            ax.text(x[i] + w/2, actual[i] + 1, f"{actual[i]}%", ha="center", fontsize=9, weight="bold")
        st.pyplot(fig)
    else:
        st.warning(budget_stats["error"])

# ------------------------------------------
# TAB 4: OUTLIERS & BEHAVIORAL PATTERNS
# ------------------------------------------
with tab4:
    st.subheader("Spending Anomalies & Payment Rail Distribution")
    anomalies = detect_overspending_and_anomalies(filtered_df)
    
    c1, c2 = st.columns(2)
    with c1:
        st.markdown(f"#### 🔍 Statistical Expense Outliers (> ₹{anomalies['outlier_threshold']:,.2f})")
        st.caption("Transactions flagged using 1.5 * Interquartile Range (IQR) technique.")
        if anomalies["top_outliers"]:
            outliers_df = pd.DataFrame(anomalies["top_outliers"])
            st.dataframe(outliers_df.style.format({"Amount": "₹{:,.2f}"}), use_container_width=True)
        else:
            st.success("No extreme spending anomalies detected!")
            
    with c2:
        st.markdown("#### 💳 Payment Rails Breakdown")
        pay_df = filtered_df[filtered_df["Type"] == "Expense"].groupby("Payment_Method")["Amount"].sum().reset_index()
        fig, ax = plt.subplots(figsize=(6, 4))
        sns.barplot(data=pay_df, x="Amount", y="Payment_Method", palette="crest", ax=ax)
        ax.xaxis.set_major_formatter('₹{x:,.0f}')
        st.pyplot(fig)

# ------------------------------------------
# TAB 5: DATA EXPLORER & INSIGHTS REPORT
# ------------------------------------------
with tab5:
    st.subheader("Executive Insights & Natural Language Report")
    insights_text = generate_automated_insights(filtered_df)
    st.text_area("Generated Executive Summary", insights_text, height=300)
    
    st.markdown("---")
    st.subheader("Raw Transaction Data Explorer")
    st.dataframe(filtered_df, use_container_width=True)
    
    # Download Button
    csv_bytes = filtered_df.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="📥 Export Filtered Data as CSV",
        data=csv_bytes,
        file_name="expenses_export.csv",
        mime="text/csv"
    )
