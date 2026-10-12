"""
src/generate_data.py
--------------------
Generates a realistic, synthetic financial expense and income dataset
designed for data science, financial analytics, and dashboarding.
"""

import os
import sys
import random
import numpy as np
import pandas as pd
from datetime import datetime, timedelta

if sys.platform.startswith("win"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

def generate_synthetic_expenses(
    output_path: str = "data/raw_expenses.csv",
    num_records: int = 750,
    seed: int = 42
) -> pd.DataFrame:
    """
    Generates a realistic synthetic personal/SME transaction dataset.
    
    Includes:
    - Monthly recurring salary and freelance income
    - Fixed recurring expenses (Rent, Wi-Fi, Electricity, Subscriptions)
    - Variable everyday expenses (Food, Groceries, Shopping, Travel, Entertainment)
    - Realistic payment methods (UPI, Credit Card, Debit Card, Net Banking, Cash)
    - Slight noise (case inconsistencies, extra spaces) to simulate raw messy data.
    """
    np.random.seed(seed)
    random.seed(seed)
    
    start_date = datetime(2024, 1, 1)
    end_date = datetime(2024, 12, 31)
    days_range = (end_date - start_date).days
    
    records = []
    txn_counter = 1001

    # 1. Generate monthly fixed Income (Salary credited on 1st-3rd of every month)
    monthly_dates = pd.date_range(start="2024-01-01", end="2024-12-01", freq="MS")
    for d in monthly_dates:
        salary_date = d + timedelta(days=random.randint(0, 2))
        records.append({
            "Transaction_ID": f"TXN{txn_counter}",
            "Date": salary_date.strftime("%Y-%m-%d"),
            "Category": "Salary",
            "Description": "Monthly Corporate Salary Credit",
            "Amount": round(random.uniform(55000, 65000), 2),
            "Type": "Income",
            "Payment_Method": "Net Banking"
        })
        txn_counter += 1
        
        # Fixed Rent & Maintenance
        rent_date = d + timedelta(days=random.randint(3, 5))
        records.append({
            "Transaction_ID": f"TXN{txn_counter}",
            "Date": rent_date.strftime("%Y-%m-%d"),
            "Category": "Rent & Housing",
            "Description": "Apartment Monthly Rent & Society Maintenance",
            "Amount": 18500.00,
            "Type": "Expense",
            "Payment_Method": "Net Banking"
        })
        txn_counter += 1

        # Fixed Utilities (Electricity, Wi-Fi, Water)
        util_date = d + timedelta(days=random.randint(6, 10))
        records.append({
            "Transaction_ID": f"TXN{txn_counter}",
            "Date": util_date.strftime("%Y-%m-%d"),
            "Category": "Bills & Utilities",
            "Description": "Fiber Broadband & Power Bill",
            "Amount": round(random.uniform(2200, 3200), 2),
            "Type": "Expense",
            "Payment_Method": "UPI"
        })
        txn_counter += 1

        # Subscriptions
        sub_date = d + timedelta(days=random.randint(10, 15))
        records.append({
            "Transaction_ID": f"TXN{txn_counter}",
            "Date": sub_date.strftime("%Y-%m-%d"),
            "Category": "Subscriptions",
            "Description": "Netflix, Spotify & Cloud Storage",
            "Amount": 1199.00,
            "Type": "Expense",
            "Payment_Method": "Credit Card"
        })
        txn_counter += 1

    # 2. Variable categories pool
    variable_categories = [
        ("Food & Dining", ["Swiggy Order", "Zomato Dinner", "Coffee Shop", "Office Cafeteria", "Weekend Restaurant"], (120, 1400), ["UPI", "Credit Card", "Cash"]),
        ("Groceries", ["Supermarket Grocery", "Fresh Vegetables", "Milk & Dairy", "D-Mart Hypermarket"], (350, 4200), ["UPI", "Debit Card", "Credit Card"]),
        ("Transportation", ["Uber Cab Ride", "Metro Card Recharge", "Fuel Petrol", "Auto Fare", "Ola Ride"], (60, 2100), ["UPI", "Cash", "Debit Card"]),
        ("Entertainment", ["Movie Tickets Cinema", "Gaming & Events", "Weekend Outing", "Concert Pass"], (300, 3500), ["Credit Card", "UPI"]),
        ("Shopping", ["Amazon Shopping", "Clothing & Apparel", "Electronics & Gadgets", "Footwear"], (600, 7500), ["Credit Card", "Net Banking", "UPI"]),
        ("Health & Fitness", ["Pharmacy Medicine", "Gym Membership", "Doctor Consultation", "Health Supplements"], (200, 3000), ["UPI", "Debit Card", "Cash"]),
        ("Freelance & Side Income", ["Consulting Fee", "Freelance Web Project", "Stock Dividend Payout", "Bonus"], (5000, 22000), ["Net Banking", "UPI"])
    ]

    # Generate remaining variable transactions
    remaining_count = num_records - len(records)
    for _ in range(remaining_count):
        random_days = random.randint(0, days_range)
        txn_date = start_date + timedelta(days=random_days)
        
        # Pick category with weighted probability (Food, Groceries, Travel occur more frequently)
        cat_choice = random.choices(
            variable_categories,
            weights=[0.30, 0.22, 0.18, 0.08, 0.10, 0.07, 0.05],
            k=1
        )[0]
        
        cat_name, descriptions, amount_range, pay_methods = cat_choice
        desc = random.choice(descriptions)
        amount = round(random.uniform(amount_range[0], amount_range[1]), 2)
        txn_type = "Income" if cat_name == "Freelance & Side Income" else "Expense"
        pay_method = random.choice(pay_methods)

        # Introduce slight raw data noise for realistic data cleaning:
        # e.g., occasional mixed case or trailing whitespace in 5% of records
        if random.random() < 0.05:
            cat_name = f" {cat_name.lower()} "
        if random.random() < 0.04:
            txn_type = txn_type.lower()
            
        records.append({
            "Transaction_ID": f"TXN{txn_counter}",
            "Date": txn_date.strftime("%Y-%m-%d"),
            "Category": cat_name,
            "Description": desc,
            "Amount": amount,
            "Type": txn_type,
            "Payment_Method": pay_method
        })
        txn_counter += 1

    df = pd.DataFrame(records)
    
    # Shuffle records so dates are not pre-sorted
    df = df.sample(frac=1, random_state=seed).reset_index(drop=True)
    
    # Inject a couple of deliberate duplicate rows to showcase duplicate removal
    df = pd.concat([df, df.iloc[[5, 12]]], ignore_index=True)

    # Ensure target directory exists
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    df.to_csv(output_path, index=False)
    print(f"✅ Generated {len(df)} synthetic records saved to '{output_path}'.")
    return df

if __name__ == "__main__":
    generate_synthetic_expenses()
