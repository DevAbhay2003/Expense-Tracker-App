"""
src/analytics.py
----------------
Core financial intelligence and analytics engine.
Computes KPIs, spending patterns, budget adherence (50/30/20 rule),
anomaly/overspending detection, and generates automated executive insights.
"""

import sys
import pandas as pd
import numpy as np
from typing import Dict, Any, Tuple

if sys.platform.startswith("win"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

def compute_financial_kpis(df: pd.DataFrame) -> Dict[str, Any]:
    """
    Computes top-level summary metrics (KPIs) for the dataset.
    """
    income_df = df[df["Type"] == "Income"]
    expense_df = df[df["Type"] == "Expense"]
    
    total_income = income_df["Amount"].sum()
    total_expense = expense_df["Amount"].sum()
    net_savings = total_income - total_expense
    savings_rate = (net_savings / total_income * 100) if total_income > 0 else 0
    
    num_months = max(df["Year_Month"].nunique(), 1)
    avg_monthly_expense = total_expense / num_months
    avg_monthly_income = total_income / num_months
    
    # Days spanned
    date_min = df["Date"].min()
    date_max = df["Date"].max()
    days_count = max((date_max - date_min).days, 1) if pd.notnull(date_min) and pd.notnull(date_max) else 30
    daily_burn_rate = total_expense / days_count

    return {
        "total_income": round(total_income, 2),
        "total_expense": round(total_expense, 2),
        "net_savings": round(net_savings, 2),
        "savings_rate_pct": round(savings_rate, 2),
        "avg_monthly_income": round(avg_monthly_income, 2),
        "avg_monthly_expense": round(avg_monthly_expense, 2),
        "daily_burn_rate": round(daily_burn_rate, 2),
        "num_transactions": len(df),
        "num_expense_txns": len(expense_df),
        "num_income_txns": len(income_df)
    }

def get_category_breakdown(df: pd.DataFrame) -> pd.DataFrame:
    """
    Computes spend totals, transaction counts, average ticket size,
    and proportion percentage per expense category.
    """
    expense_df = df[df["Type"] == "Expense"]
    total_expense = expense_df["Amount"].sum()
    
    cat_summary = expense_df.groupby("Category")["Amount"].agg(
        Total_Spend="sum",
        Txn_Count="count",
        Avg_Ticket_Size="mean"
    ).reset_index()
    
    cat_summary["Percentage_Share"] = (cat_summary["Total_Spend"] / total_expense * 100).round(2)
    cat_summary["Total_Spend"] = cat_summary["Total_Spend"].round(2)
    cat_summary["Avg_Ticket_Size"] = cat_summary["Avg_Ticket_Size"].round(2)
    cat_summary = cat_summary.sort_values(by="Total_Spend", ascending=False).reset_index(drop=True)
    
    return cat_summary

def get_monthly_trends(df: pd.DataFrame) -> pd.DataFrame:
    """
    Computes monthly timeline aggregates: Income, Expense, Net Savings,
    and Month-over-Month (MoM) expense growth.
    """
    monthly = df.groupby(["Year_Month", "Type"])["Amount"].sum().unstack(fill_value=0).reset_index()
    
    if "Income" not in monthly.columns:
        monthly["Income"] = 0.0
    if "Expense" not in monthly.columns:
        monthly["Expense"] = 0.0
        
    monthly["Net_Savings"] = monthly["Income"] - monthly["Expense"]
    monthly["Savings_Rate_Pct"] = np.where(
        monthly["Income"] > 0,
        ((monthly["Net_Savings"] / monthly["Income"]) * 100).round(2),
        0.0
    )
    
    # Month-over-Month Expense Growth Rate
    monthly["Expense_MoM_Growth_Pct"] = monthly["Expense"].pct_change().mul(100).round(2).fillna(0)
    
    return monthly

def evaluate_50_30_20_rule(df: pd.DataFrame) -> Dict[str, Any]:
    """
    Evaluates compliance against the personal finance 50/30/20 guideline:
    - 50% Needs (Housing, Utilities, Groceries, Healthcare)
    - 30% Wants (Dining, Shopping, Entertainment, Subscriptions)
    - 20% Savings (Retained income)
    """
    income = df[df["Type"] == "Income"]["Amount"].sum()
    if income == 0:
        return {"error": "Income is zero; cannot calculate 50/30/20 rule."}
        
    needs_spend = df[(df["Type"] == "Expense") & (df["Budget_Bucket"] == "Needs")]["Amount"].sum()
    wants_spend = df[(df["Type"] == "Expense") & (df["Budget_Bucket"] == "Wants")]["Amount"].sum()
    misc_spend = df[(df["Type"] == "Expense") & (df["Budget_Bucket"] == "Miscellaneous")]["Amount"].sum()
    actual_savings = income - (needs_spend + wants_spend + misc_spend)
    
    needs_pct = round((needs_spend / income) * 100, 2)
    wants_pct = round((wants_spend / income) * 100, 2)
    savings_pct = round((actual_savings / income) * 100, 2)
    misc_pct = round((misc_spend / income) * 100, 2)
    
    return {
        "needs_pct": needs_pct,
        "wants_pct": wants_pct,
        "savings_pct": savings_pct,
        "misc_pct": misc_pct,
        "needs_compliant": needs_pct <= 50.0,
        "wants_compliant": wants_pct <= 30.0,
        "savings_compliant": savings_pct >= 20.0
    }

def detect_overspending_and_anomalies(df: pd.DataFrame) -> Dict[str, Any]:
    """
    Identifies financial irregularities, overspending months, and transaction outliers.
    """
    expense_df = df[df["Type"] == "Expense"]
    
    # 1. Deficit Months (Expense > Income)
    monthly = get_monthly_trends(df)
    deficit_months = monthly[monthly["Net_Savings"] < 0][["Year_Month", "Income", "Expense", "Net_Savings"]].to_dict(orient="records")
    
    # 2. Transaction Outliers using 1.5 * IQR rule
    q1 = expense_df["Amount"].quantile(0.25)
    q3 = expense_df["Amount"].quantile(0.75)
    iqr = q3 - q1
    outlier_threshold = q3 + (1.5 * iqr)
    outliers_df = expense_df[expense_df["Amount"] > outlier_threshold][["Date", "Category", "Description", "Amount", "Payment_Method"]].sort_values(by="Amount", ascending=False)
    
    # 3. Peak spending day of the week
    weekday_agg = expense_df.groupby("Weekday")["Amount"].sum().sort_values(ascending=False)
    peak_weekday = weekday_agg.index[0] if not weekday_agg.empty else "N/A"

    return {
        "deficit_months": deficit_months,
        "outlier_threshold": round(outlier_threshold, 2),
        "outlier_transactions_count": len(outliers_df),
        "top_outliers": outliers_df.head(5).to_dict(orient="records"),
        "peak_spending_weekday": peak_weekday
    }

def generate_automated_insights(df: pd.DataFrame) -> str:
    """
    Generates actionable, business-ready natural language insights
    synthesizing KPIs, trends, budget adherence, and cost leaks.
    """
    kpis = compute_financial_kpis(df)
    cat_df = get_category_breakdown(df)
    monthly = get_monthly_trends(df)
    budget = evaluate_50_30_20_rule(df)
    anomalies = detect_overspending_and_anomalies(df)
    
    top_cat = cat_df.iloc[0] if not cat_df.empty else None
    highest_spend_month = monthly.loc[monthly["Expense"].idxmax()] if not monthly.empty else None
    
    insights = []
    insights.append("=======================================================")
    insights.append("        EXECUTIVE FINANCIAL HEALTH REPORT             ")
    insights.append("=======================================================\n")
    
    # 1. Macro Summary
    insights.append("📌 1. MACRO SUMMARY & SAVINGS PERFORMANCE:")
    insights.append(f"  • Cumulative Cash Inflow:  ₹{kpis['total_income']:,.2f}")
    insights.append(f"  • Cumulative Cash Outflow: ₹{kpis['total_expense']:,.2f}")
    insights.append(f"  • Net Savings Accumulated: ₹{kpis['net_savings']:,.2f}")
    insights.append(f"  • Overall Savings Rate:    {kpis['savings_rate_pct']}%")
    if kpis["savings_rate_pct"] >= 25:
        insights.append("  • Status: 🟢 EXCELLENT - Substantial liquidity cushion maintained.")
    elif kpis["savings_rate_pct"] >= 15:
        insights.append("  • Status: 🟡 MODERATE - Meets basic emergency fund guidelines.")
    else:
        insights.append("  • Status: 🔴 VULNERABLE - High burn rate; vulnerable to liquidity shocks.")
    
    # 2. Category Concentration
    insights.append("\n📌 2. CATEGORY CONCENTRATION:")
    if top_cat is not None:
        insights.append(f"  • Largest Outflow Driver:  '{top_cat['Category']}' accounting for ₹{top_cat['Total_Spend']:,.2f} ({top_cat['Percentage_Share']}% of total expenses).")
        if len(cat_df) > 1:
            second_cat = cat_df.iloc[1]
            insights.append(f"  • Secondary Cost Driver:   '{second_cat['Category']}' with ₹{second_cat['Total_Spend']:,.2f} ({second_cat['Percentage_Share']}%).")
            
    # 3. 50/30/20 Rule Adherence
    insights.append("\n📌 3. BUDGET ADHERENCE (50/30/20 RULE):")
    insights.append(f"  • Needs Allocation:   {budget['needs_pct']}% (Benchmark: ≤ 50%) -> {'✅ Balanced' if budget['needs_compliant'] else '⚠️ Over budget'}")
    insights.append(f"  • Wants Allocation:   {budget['wants_pct']}% (Benchmark: ≤ 30%) -> {'✅ Controlled' if budget['wants_compliant'] else '⚠️ Discretionary lifestyle creep detected'}")
    insights.append(f"  • Savings Allocation: {budget['savings_pct']}% (Benchmark: ≥ 20%) -> {'✅ Goal achieved' if budget['savings_compliant'] else '⚠️ Below savings target'}")
    
    # 4. Volatility & Deficits
    insights.append("\n📌 4. VOLATILITY & DEFICIT MONITORING:")
    if highest_spend_month is not None:
        insights.append(f"  • Peak Burn Month: {highest_spend_month['Year_Month']} (Total Outflow: ₹{highest_spend_month['Expense']:,.2f})")
    if anomalies["deficit_months"]:
        insights.append(f"  • ⚠️ Deficit Alert: {len(anomalies['deficit_months'])} month(s) operated at a net loss (Expenses > Income).")
        for d in anomalies["deficit_months"]:
            insights.append(f"     - {d['Year_Month']}: Deficit of ₹{abs(d['Net_Savings']):,.2f}")
    else:
        insights.append("  • 🛡️ Zero Deficit Months: Net monthly cash flow remained positive in every period.")
        
    insights.append(f"  • Peak Discretionary Activity Day: {anomalies['peak_spending_weekday']}.")
    
    # 5. Strategic Recommendations
    insights.append("\n📌 5. ACTIONABLE FINANCIAL RECOMMENDATIONS:")
    insights.append(f"  1. Cap '{top_cat['Category'] if top_cat is not None else 'Discretionary'}' spending using predefined monthly threshold limits.")
    if budget["wants_pct"] > 30:
        insights.append("  2. Trim dining and entertainment subscriptions to bring 'Wants' down to the 30% benchmark.")
    insights.append("  3. Automate recurring transfers to an investment/emergency fund on the 1st of every month to 'pay yourself first'.")
    insights.append("=======================================================")
    
    return "\n".join(insights)

if __name__ == "__main__":
    df = pd.read_csv("data/cleaned_expenses.csv")
    print(generate_automated_insights(df))
