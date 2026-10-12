"""
src/visualizations.py
---------------------
Generates presentation-grade financial charts using Matplotlib and Seaborn.
Saves all visual artifacts to the outputs/ directory.
"""

import os
import sys
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np

if sys.platform.startswith("win"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

# Configure standard professional chart styling
sns.set_theme(style="whitegrid", font="sans-serif")
plt.rcParams["font.family"] = "sans-serif"
plt.rcParams["figure.autolayout"] = True

def plot_category_distribution(df: pd.DataFrame, output_dir: str = "outputs"):
    """
    Creates a dual-panel figure:
    - Left: Bar chart of total spend per category with currency labels
    - Right: Donut chart showing percentage expense distribution
    """
    expense_df = df[df["Type"] == "Expense"]
    cat_summary = expense_df.groupby("Category")["Amount"].sum().sort_values(ascending=False)
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6))
    
    # 1. Bar Chart
    colors = sns.color_palette("mako", len(cat_summary))
    bars = ax1.barh(cat_summary.index, cat_summary.values, color=colors)
    ax1.set_title("Total Outflow by Category (₹)", fontsize=14, weight="bold", pad=12)
    ax1.set_xlabel("Total Spend (₹)", fontsize=11)
    ax1.invert_yaxis()  # Largest on top
    
    for bar in bars:
        width = bar.get_width()
        ax1.text(width + (width * 0.01), bar.get_y() + bar.get_height()/2,
                 f"₹{width:,.0f}", ha='left', va='center', fontsize=9, weight="bold")

    # 2. Donut Chart
    wedges, texts, autotexts = ax2.pie(
        cat_summary.values,
        labels=cat_summary.index,
        autopct="%1.1f%%",
        startangle=140,
        pctdistance=0.8,
        colors=sns.color_palette("Set2", len(cat_summary)),
        wedgeprops=dict(width=0.4, edgecolor='white', linewidth=2)
    )
    for autotext in autotexts:
        autotext.set_fontsize(9)
        autotext.set_weight("bold")
    ax2.set_title("Expense Share Distribution", fontsize=14, weight="bold", pad=12)
    
    plt.suptitle("Category-Wise Financial Exposure Analysis", fontsize=16, weight="bold")
    save_path = os.path.join(output_dir, "category_distribution.png")
    plt.savefig(save_path, dpi=300, bbox_inches="tight")
    plt.close()
    print(f"📊 Saved: {save_path}")

def plot_monthly_trends(df: pd.DataFrame, output_dir: str = "outputs"):
    """
    Plots a dual-series line & area plot comparing Monthly Income vs Monthly Expense,
    highlighting the net savings spread over time.
    """
    monthly = df.groupby(["Year_Month", "Type"])["Amount"].sum().unstack(fill_value=0).reset_index()
    if "Income" not in monthly.columns: monthly["Income"] = 0
    if "Expense" not in monthly.columns: monthly["Expense"] = 0
        
    fig, ax = plt.subplots(figsize=(13, 6))
    
    x = np.arange(len(monthly))
    width = 0.35
    
    ax.bar(x - width/2, monthly["Income"], width, label="Cash Inflow (Income)", color="#2ecc71", alpha=0.85)
    ax.bar(x + width/2, monthly["Expense"], width, label="Cash Outflow (Expense)", color="#e74c3c", alpha=0.85)
    
    # Net savings line overlay
    ax.plot(x, monthly["Income"] - monthly["Expense"], marker="o", color="#3498db", linewidth=2.5, label="Net Savings")
    
    ax.set_xticks(x)
    ax.set_xticklabels(monthly["Year_Month"], rotation=40, ha="right", fontsize=10)
    ax.set_title("Monthly Financial Trajectory: Inflow vs. Outflow & Net Savings", fontsize=15, weight="bold", pad=15)
    ax.set_ylabel("Amount (₹)", fontsize=11)
    ax.yaxis.set_major_formatter('₹{x:,.0f}')
    ax.legend(frameon=True, facecolor="white", loc="upper left")
    
    save_path = os.path.join(output_dir, "monthly_trend.png")
    plt.savefig(save_path, dpi=300, bbox_inches="tight")
    plt.close()
    print(f"📊 Saved: {save_path}")

def plot_weekday_spending(df: pd.DataFrame, output_dir: str = "outputs"):
    """
    Analyzes day-of-week spending velocity and transaction density.
    """
    expense_df = df[df["Type"] == "Expense"]
    order = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    
    weekday_summary = expense_df.groupby("Weekday")["Amount"].agg(
        Total_Spend="sum",
        Txn_Count="count"
    ).reindex(order).reset_index()
    
    fig, ax1 = plt.subplots(figsize=(11, 5))
    
    color_spend = "#4b7bec"
    color_count = "#fc5c65"
    
    bars = ax1.bar(weekday_summary["Weekday"], weekday_summary["Total_Spend"], color=color_spend, alpha=0.75, label="Total Spend (₹)")
    ax1.set_ylabel("Total Spend (₹)", color=color_spend, fontsize=11, weight="bold")
    ax1.tick_params(axis="y", labelcolor=color_spend)
    ax1.yaxis.set_major_formatter('₹{x:,.0f}')
    
    ax2 = ax1.twinx()
    ax2.plot(weekday_summary["Weekday"], weekday_summary["Txn_Count"], color=color_count, marker="s", linewidth=2.5, label="Transaction Count")
    ax2.set_ylabel("Transaction Count", color=color_count, fontsize=11, weight="bold")
    ax2.tick_params(axis="y", labelcolor=color_count)
    ax2.grid(False)
    
    plt.title("Weekly Spending Velocity & Transaction Frequency", fontsize=14, weight="bold", pad=12)
    save_path = os.path.join(output_dir, "weekday_spending.png")
    plt.savefig(save_path, dpi=300, bbox_inches="tight")
    plt.close()
    print(f"📊 Saved: {save_path}")

def plot_payment_methods(df: pd.DataFrame, output_dir: str = "outputs"):
    """
    Visualizes transaction value and volume partitioned by payment rails (UPI, Card, Net Banking).
    """
    pay_summary = df[df["Type"] == "Expense"].groupby("Payment_Method")["Amount"].sum().sort_values(ascending=False)
    
    plt.figure(figsize=(9, 5))
    palette = sns.color_palette("crest", len(pay_summary))
    sns.barplot(x=pay_summary.values, y=pay_summary.index, hue=pay_summary.index, palette=palette, legend=False)
    
    plt.title("Payment Channel Utilization (Total Outflow)", fontsize=14, weight="bold", pad=12)
    plt.xlabel("Total Outflow (₹)", fontsize=11)
    plt.ylabel("Payment Method", fontsize=11)
    
    for i, v in enumerate(pay_summary.values):
        plt.text(v + (v * 0.01), i, f"₹{v:,.0f}", va="center", fontsize=10, weight="bold")
        
    save_path = os.path.join(output_dir, "payment_method_breakdown.png")
    plt.savefig(save_path, dpi=300, bbox_inches="tight")
    plt.close()
    print(f"📊 Saved: {save_path}")

def plot_budget_benchmark(df: pd.DataFrame, output_dir: str = "outputs"):
    """
    Visualizes actual spending allocation against the classic 50/30/20 Personal Finance Rule.
    """
    income = df[df["Type"] == "Income"]["Amount"].sum()
    if income == 0: return
    
    needs = df[(df["Type"] == "Expense") & (df["Budget_Bucket"] == "Needs")]["Amount"].sum()
    wants = df[(df["Type"] == "Expense") & (df["Budget_Bucket"] == "Wants")]["Amount"].sum()
    savings = income - df[df["Type"] == "Expense"]["Amount"].sum()
    
    actual_pcts = [
        round((needs / income) * 100, 1),
        round((wants / income) * 100, 1),
        round((savings / income) * 100, 1)
    ]
    target_pcts = [50.0, 30.0, 20.0]
    categories = ["Needs (≤ 50%)", "Wants (≤ 30%)", "Savings (≥ 20%)"]
    
    x = np.arange(len(categories))
    width = 0.35
    
    fig, ax = plt.subplots(figsize=(9, 5))
    ax.bar(x - width/2, target_pcts, width, label="Target Benchmark %", color="#95a5a6", alpha=0.7)
    ax.bar(x + width/2, actual_pcts, width, label="Actual Allocation %", color=["#3498db", "#e67e22", "#2ecc71"])
    
    ax.set_ylabel("Share of Inflow (%)", fontsize=11)
    ax.set_title("Financial Health Audit: 50/30/20 Budget Rule vs. Actual Spend", fontsize=14, weight="bold", pad=12)
    ax.set_xticks(x)
    ax.set_xticklabels(categories, fontsize=11, weight="bold")
    ax.set_ylim(0, max(max(actual_pcts), 60) + 10)
    ax.legend(frameon=True, facecolor="white")
    
    for i in range(len(categories)):
        ax.text(x[i] - width/2, target_pcts[i] + 1, f"{target_pcts[i]}%", ha="center", fontsize=9)
        ax.text(x[i] + width/2, actual_pcts[i] + 1, f"{actual_pcts[i]}%", ha="center", fontsize=10, weight="bold")
        
    save_path = os.path.join(output_dir, "budget_vs_actual.png")
    plt.savefig(save_path, dpi=300, bbox_inches="tight")
    plt.close()
    print(f"📊 Saved: {save_path}")

def generate_all_visualizations(df: pd.DataFrame, output_dir: str = "outputs"):
    """
    Executes all visualization generators and saves charts to disk.
    """
    os.makedirs(output_dir, exist_ok=True)
    print(f"🎨 Generating analytics visualizations in '{output_dir}/'...")
    plot_category_distribution(df, output_dir)
    plot_monthly_trends(df, output_dir)
    plot_weekday_spending(df, output_dir)
    plot_payment_methods(df, output_dir)
    plot_budget_benchmark(df, output_dir)
    print("✅ All charts generated and saved successfully!")

if __name__ == "__main__":
    df = pd.read_csv("data/cleaned_expenses.csv")
    generate_all_visualizations(df)
