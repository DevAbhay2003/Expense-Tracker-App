"""
src/data_preprocessing.py
-------------------------
Handles data cleaning, normalization, validation, and feature engineering
for expense tracking data.
"""

import os
import sys
import pandas as pd
import numpy as np

if sys.platform.startswith("win"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

def classify_budget_bucket(row):
    """
    Classifies transactions into the classic 50/30/20 financial planning rule:
    - Needs (50%): Housing, Utilities, Basic Groceries, Healthcare
    - Wants (30%): Dining, Entertainment, Shopping, Streaming
    - Income/Savings: Inflows
    """
    txn_type = row.get("Type", "Expense")
    if txn_type == "Income":
        return "Income"
    
    cat = str(row.get("Category", "")).lower()
    if any(k in cat for k in ["rent", "housing", "bill", "utilit", "grocer", "health", "medicine"]):
        return "Needs"
    elif any(k in cat for k in ["dining", "food", "entertain", "shop", "subscript"]):
        return "Wants"
    else:
        return "Miscellaneous"

def clean_and_preprocess_data(
    input_path: str = "data/raw_expenses.csv",
    output_path: str = "data/cleaned_expenses.csv"
) -> pd.DataFrame:
    """
    Loads raw expense dataset, performs data cleaning, data type conversions,
    handles anomalies, and generates engineered time and financial features.
    """
    if not os.path.exists(input_path):
        raise FileNotFoundError(f"Input file not found at: {input_path}")
        
    print(f"🔄 Loading raw data from '{input_path}'...")
    df = pd.read_csv(input_path)
    initial_rows = len(df)
    
    # 1. Deduplication
    df = df.drop_duplicates(subset=["Transaction_ID"], keep="first")
    df = df.drop_duplicates()
    deduped_rows = len(df)
    print(f"🧹 Removed {initial_rows - deduped_rows} duplicate record(s).")

    # 2. String standardization (stripping spaces, title case)
    string_cols = ["Category", "Description", "Type", "Payment_Method"]
    for col in string_cols:
        if col in df.columns:
            df[col] = df[col].astype(str).str.strip().str.title()

    # 3. Handle Missing Values
    critical_cols = ["Date", "Category", "Amount", "Type"]
    missing_before = df[critical_cols].isnull().sum().sum()
    df = df.dropna(subset=critical_cols)
    if missing_before > 0:
        print(f"🧹 Handled {missing_before} missing field value(s).")

    # 4. Data Type Conversions
    df["Date"] = pd.to_datetime(df["Date"], errors="coerce")
    df["Amount"] = pd.to_numeric(df["Amount"], errors="coerce")
    
    # Drop records where Date or Amount couldn't be parsed
    df = df.dropna(subset=["Date", "Amount"])
    df = df[df["Amount"] > 0]  # Transactions must be positive

    # 5. Sort chronologically
    df = df.sort_values(by="Date").reset_index(drop=True)

    # 6. Feature Engineering (Date & Time components)
    df["Year"] = df["Date"].dt.year
    df["Month_Num"] = df["Date"].dt.month
    df["Month_Name"] = df["Date"].dt.month_name()
    df["Year_Month"] = df["Date"].dt.strftime("%Y-%m")
    df["Day"] = df["Date"].dt.day
    df["Weekday"] = df["Date"].dt.day_name()
    df["Is_Weekend"] = df["Date"].dt.dayofweek.isin([5, 6])
    df["Quarter"] = "Q" + df["Date"].dt.quarter.astype(str)

    # 7. Financial Feature Engineering: 50/30/20 Category Bucketing
    df["Budget_Bucket"] = df.apply(classify_budget_bucket, axis=1)

    # 8. Save cleaned dataset
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    df.to_csv(output_path, index=False)
    print(f"✅ Data cleaning complete! {len(df)} records saved to '{output_path}'.")
    
    return df

if __name__ == "__main__":
    clean_and_preprocess_data()
