"""
main.py
-------
Master Execution Pipeline for the Expense Tracker App (Data Science Project).
Executes synthetic data generation, data cleaning, financial analytics,
automated visualization generation, and executive insight reporting.
"""

import os
import sys

# Ensure UTF-8 stdout on Windows console
if sys.platform.startswith("win"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

from src.generate_data import generate_synthetic_expenses
from src.data_preprocessing import clean_and_preprocess_data
from src.analytics import (
    compute_financial_kpis,
    get_category_breakdown,
    get_monthly_trends,
    evaluate_50_30_20_rule,
    detect_overspending_and_anomalies,
    generate_automated_insights
)
from src.visualizations import generate_all_visualizations

def run_pipeline():
    print("=" * 65)
    print(" 🚀 EXPENSE TRACKER APP: DATA SCIENCE & ANALYTICS PIPELINE")
    print("=" * 65)

    # Step 1: Synthetic Data Generation
    print("\n[Step 1/5] Synthesizing realistic financial transaction history...")
    raw_df = generate_synthetic_expenses(
        output_path="data/raw_expenses.csv",
        num_records=750,
        seed=42
    )
    print(f"  • Generated: {len(raw_df)} transactions spanning 12 months.")

    # Step 2: Data Preprocessing & Cleaning
    print("\n[Step 2/5] Cleaning, normalizing, and feature engineering...")
    cleaned_df = clean_and_preprocess_data(
        input_path="data/raw_expenses.csv",
        output_path="data/cleaned_expenses.csv"
    )
    print(f"  • Preprocessed: {len(cleaned_df)} validated records ready for analytics.")

    # Step 3: Analytical Aggregations
    print("\n[Step 3/5] Computing financial KPIs and aggregations...")
    kpis = compute_financial_kpis(cleaned_df)
    print(f"  • Total Income:   ₹{kpis['total_income']:,.2f}")
    print(f"  • Total Outflow:  ₹{kpis['total_expense']:,.2f}")
    print(f"  • Net Savings:    ₹{kpis['net_savings']:,.2f} ({kpis['savings_rate_pct']}%)")
    print(f"  • Daily Burn:     ₹{kpis['daily_burn_rate']:,.2f}/day")

    # Step 4: Visualizations
    print("\n[Step 4/5] Rendering and saving analytical charts...")
    generate_all_visualizations(cleaned_df, output_dir="outputs")

    # Step 5: Automated Executive Insights
    print("\n[Step 5/5] Generating automated executive financial report...")
    report_text = generate_automated_insights(cleaned_df)
    
    # Save insights report to disk
    report_file = os.path.join("outputs", "financial_summary_report.txt")
    with open(report_file, "w", encoding="utf-8") as f:
        f.write(report_text)
    print(f"  • Saved executive insights to '{report_file}'.\n")

    # Print the report to stdout
    print(report_text)

    print("\n" + "=" * 65)
    print(" 🎉 PIPELINE RUN COMPLETE!")
    print("  To launch the interactive web dashboard, run:")
    print("     streamlit run app.py")
    print("=" * 65 + "\n")

if __name__ == "__main__":
    run_pipeline()
